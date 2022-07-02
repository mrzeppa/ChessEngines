import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.optimizers as optimizers
from tensorflow.keras.callbacks import ModelCheckpoint

model = None

def build_model(conv_size):
  board3d = layers.Input(shape=(14, 8, 8))

    x = board3d
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(x)
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(x)
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(x)
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, 'relu')(x)
    x = layers.Dense(1, 'sigmoid')(x)

    return models.Model(inputs=board3d, outputs=x)


def trainModel():
    model = build_model(32)
    model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
    model.summary()
    checkpoint_filepath = '/tmp/checkpoint/'
    model_checkpointing_callback = ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_best_only=True,
    )
    model.fit(x_train, y_train,
            batch_size=2048,
            epochs=1000,
            verbose=1,
            validation_split=0.1,
            callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                       callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4),
                       model_checkpointing_callback])

    model.save('model.h5')

