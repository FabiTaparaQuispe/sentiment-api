"""Entrena el modelo y lo guarda. Se corre en el build de la imagen."""

from app.model import MODEL_PATH, train


def main() -> None:
    train(save=True)
    print(f"Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    main()
