import numpy as np
import tensorflow as tf


class AutoEncoder():
    def __init__(self):
        self.autoencoder = None
        self.encoder = None
        self.decoder = None
    
    # Train
    def fit(self, X, n_epochs=50, batch_size=256):
        indices_fracs = split(fracs=[0.9, 0.1], N=len(X), seed=0)
        X_train, X_valid = X[indices_fracs[0]], X[indices_fracs[1]]
        self.autoencoder.fit(X_train, X_train,
                             epochs = n_epochs,
                             batch_size = batch_size,
                             shuffle = True,
                             validation_data = (X_valid, X_valid))

    # Inference
    def predict(self, X):
        return self.encoder.predict(X)
    
    # Set neural network architecture
    def set_arch(self):
        shape_img = 0
        shape_img_flattened = (np.prod(list(shape_img)),)

        n_hidden_1, n_hidden_2, n_hidden_3 = 16, 8, 8
        conv_kernel = (3, 3) # convolution kernel
        pool_kernel = (2, 2) # pooling kernel

        input = tf.keras.layers.Input(shape=shape_img)
        x = tf.keras.layers.Conv2D(n_hidden_1, conv_kernel, activation='relu', padding='same')(input)
        x = tf.keras.layers.MaxPooling2D(pool_kernel, padding='same')(x)
        x = tf.keras.layers.Conv2D(n_hidden_2, conv_kernel, activation='relu', padding='same')(x)
        x = tf.keras.layers.MaxPooling2D(pool_kernel, padding='same')(x)
        x = tf.keras.layers.Conv2D(n_hidden_3, conv_kernel, activation='relu', padding='same')(x)
        encoded = tf.keras.layers.MaxPooling2D(pool_kernel, padding='same')(x)

        x = tf.keras.layers.Conv2D(n_hidden_3, conv_kernel, activation='relu', padding='same')(encoded)
        x = tf.keras.layers.UpSampling2D(pool_kernel)(x)
        x = tf.keras.layers.Conv2D(n_hidden_2, conv_kernel, activation='relu', padding='same')(x)
        x = tf.keras.layers.UpSampling2D(pool_kernel)(x)
        x = tf.keras.layers.Conv2D(n_hidden_1, conv_kernel, activation='relu')(x)
        x = tf.keras.layers.UpSampling2D(pool_kernel)(x)
        decoded = tf.keras.layers.Conv2D(shape_img[2], conv_kernel, activation='sigmoid', padding='same')(x)

        # Create autoencoder model
        autoencoder = tf.keras.Model(input, decoded)
        input_autoencoder_shape = autoencoder.layers[0].input_shape[1:]
        output_autoencoder_shape = autoencoder.layers[-1].output_shape[1:]

        # Create encoder model
        encoder = tf.keras.Model(input, encoded)  # set encoder
        input_encoder_shape = encoder.layers[0].input_shape[1:]
        output_encoder_shape = encoder.layers[-1].output_shape[1:]

        # Create decoder model
        decoded_input = tf.keras.Input(shape=output_encoder_shape)
        decoded_output = autoencoder.layers[-7](decoded_input)  # Conv2D
        decoded_output = autoencoder.layers[-6](decoded_output)  # UpSampling2D
        decoded_output = autoencoder.layers[-5](decoded_output)  # Conv2D
        decoded_output = autoencoder.layers[-4](decoded_output)  # UpSampling2D
        decoded_output = autoencoder.layers[-3](decoded_output)  # Conv2D
        decoded_output = autoencoder.layers[-2](decoded_output)  # UpSampling2D
        decoded_output = autoencoder.layers[-1](decoded_output)  # Conv2D
        decoder = tf.keras.Model(decoded_input, decoded_output)
        decoder_input_shape = decoder.layers[0].input_shape[1:]
        decoder_output_shape = decoder.layers[-1].output_shape[1:]

        self.autoencoder = autoencoder
        self.encoder = encoder
        self.decoder = decoder

    # Compile
    def compile(self, loss="binary_crossentropy", optimizer="adam"):
        self.autoencoder.compile(optimizer=optimizer, loss=loss)

    # Load model architecture and weights
    def load_models(self, loss="binary_crossentropy", optimizer="adam"):
        print("Loading models...")
        self.autoencoder = tf.keras.models.load_model(self.info["autoencoderFile"])
        self.encoder = tf.keras.models.load_model(self.info["encoderFile"])
        self.decoder = tf.keras.models.load_model(self.info["decoderFile"])
        self.autoencoder.compile(optimizer=optimizer, loss=loss)
        self.encoder.compile(optimizer=optimizer, loss=loss)
        self.decoder.compile(optimizer=optimizer, loss=loss)

    # Save model architecture and weights to file
    def save_models(self):
        print("Saving models...")
        self.autoencoder.save(self.info["autoencoderFile"])
        self.encoder.save(self.info["encoderFile"])
        self.decoder.save(self.info["decoderFile"])
