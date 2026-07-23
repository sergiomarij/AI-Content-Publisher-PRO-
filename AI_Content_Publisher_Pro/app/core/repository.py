from app.core.models import Article
from app.core.session import SessionLocal


class ArticleRepository:

    @staticmethod
    def add(article: Article):

        db = SessionLocal()

        db.add(article)

        db.commit()

        db.refresh(article)

        db.close()

        return article