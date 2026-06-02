import os
import sys

MNIST_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "5 - Notebooks", "data", "mnist"
)
TRAIN_PATH = os.path.join(MNIST_DIR, "train.csv")
TEST_PATH = os.path.join(MNIST_DIR, "test.csv")


def using_tensorflow():
    print("Descargando MNIST via TensorFlow/Keras...")
    try:
        from tensorflow.keras.datasets import mnist
        import numpy as np
        import pandas as pd
    except ImportError:
        return False

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    n_train = x_train.shape[0]
    n_test = x_test.shape[0]

    train_data = []
    for i in range(n_train):
        flat = x_train[i].reshape(-1)
        row = [int(y_train[i])] + [int(p) for p in flat]
        train_data.append(row)

    test_data = []
    for i in range(n_test):
        flat = x_test[i].reshape(-1)
        row = [int(y_test[i])] + [int(p) for p in flat]
        test_data.append(row)

    columns = ["label"] + [f"pixel{j}" for j in range(784)]

    os.makedirs(MNIST_DIR, exist_ok=True)

    pd.DataFrame(train_data, columns=columns).to_csv(TRAIN_PATH, index=False)
    print(f"  -> {TRAIN_PATH} ({n_train} samples)")

    pd.DataFrame(test_data, columns=columns).to_csv(TEST_PATH, index=False)
    print(f"  -> {TEST_PATH} ({n_test} samples)")

    return True


def using_kagglehub():
    print("Descargando MNIST via kagglehub...")
    try:
        import kagglehub
        import pandas as pd
        import shutil
    except ImportError:
        return False

    path = kagglehub.dataset_download("oddrationale/mnist-in-csv")
    os.makedirs(MNIST_DIR, exist_ok=True)

    for fname in ["train.csv", "test.csv"]:
        src = os.path.join(path, fname)
        dst = os.path.join(MNIST_DIR, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  -> {dst}")
        else:
            print(f"  [WARN] {fname} no encontrado en {path}", file=sys.stderr)

    return True


def manual_instructions():
    print("No se pudo descargar automaticamente.")
    print()
    print("Opcion 1: Instala kagglehub y vuelve a intentar:")
    print("  pip install kagglehub")
    print(f"  python {os.path.relpath(__file__)}")
    print()
    print("Opcion 2: Descarga manual desde Kaggle:")
    print("  https://www.kaggle.com/datasets/oddrationale/mnist-in-csv")
    print(f"  Coloca 'train.csv' y 'test.csv' en:")
    print(f"  {os.path.abspath(MNIST_DIR)}")
    print()


def main():
    if os.path.exists(TRAIN_PATH) and os.path.exists(TEST_PATH):
        print("MNIST ya esta descargado:")
        print(f"  {TRAIN_PATH}")
        print(f"  {TEST_PATH}")
        return

    if using_tensorflow():
        print("Descarga completada via TensorFlow.")
        return

    if using_kagglehub():
        print("Descarga completada via kagglehub.")
        return

    manual_instructions()
    sys.exit(1)


if __name__ == "__main__":
    main()
