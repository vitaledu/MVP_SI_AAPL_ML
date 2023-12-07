import numpy as np
import pickle
import joblib


class Model:

    def carrega_modelo(path, scaler_path=None):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """

        if path.endswith(".pkl"):
            model = pickle.load(open(path, "rb"))
        elif path.endswith(".joblib"):
            model = joblib.load(path)
        else:
            raise Exception("Formato de arquivo não suportado")

        if scaler_path is not None:
            scaler = joblib.load(scaler_path)
            model.scaler = scaler

        return model

    def preditor(model, form):
        """Realiza a predição de uma negociação com base no modelo treinado
        """
        X_input = np.array(
            [
                form.open,
                form.high,
                form.low,
                form.close,
                form.adjclose,
            ]
        )

        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)

        # Verificando se o modelo possui um scaler atribuído
        if hasattr(model, 'scaler') and model.scaler is not None:
            # Padronização nos dados de entrada usando o scaler utilizado em X_train
            X_input_scaled = model.scaler.transform(X_input)
        else:
            X_input_scaled = X_input  # Se não houver scaler, use os dados originais



        # Adicionando uma dimensão extra para corresponder ao formato esperado pelo modelo
        volume = model.predict(X_input_scaled.reshape(1, -1))

        return int(volume[0])
