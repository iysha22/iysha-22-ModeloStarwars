from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(nullable=True)
    terrain: Mapped[str] = mapped_column(String(100))

    favorites = relationship("Favorite", back_populates="planet")

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(50))
    birth_year: Mapped[str] = mapped_column(String(20))
    height: Mapped[int] = mapped_column(nullable=True)

    favorites = relationship("Favorite", back_populates="character")

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    # Esto genera el diagrama UML automáticamente
try:
    from eralchemy2 import render_er
    render_er(db.Model, "diagram.png")
except Exception as e:
    print("No se pudo generar el diagrama:", e)
