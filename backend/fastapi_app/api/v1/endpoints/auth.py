# backend/fastapi_app/api/v1/endpoints/auth.py
# /register・/login のAPI処理
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth import hash_password, verify_password, create_access_token
from models.user import User
from schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
#            ↑入力の型チェック          ↑DBセッションを自動で注入    
    """ユーザー登録"""

    # メールアドレスの重複チェック
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスはすでに登録されています"
        )

    # パスワードを暗号化してDB保存
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """ログイン"""

    # メールアドレスでユーザーを検索
    user = db.query(User).filter(User.email == user_data.email).first()
        # SELECT * FROM users WHERE email = "xxx@gmail.com" LIMIT 1
        # と同じ意味（SQLを書かずにPythonで書ける）
        # ユーザーが存在しない or パスワードが違う場合はエラー
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません"
        )

    # JWTトークンを発行
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}