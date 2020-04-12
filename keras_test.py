from keras import models, layers
import numpy as np
#import matplotlib.pyplot as plt

def build_model(train_data):
    model = models.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if (len(smoothed_points) != 0):
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

def runModel(train_data, train_targets, test_data, test_targets):
    # K-fold validation b/c there are not many data points
    k = 2
    num_val_samples = len(train_data) // k
    num_epochs = 7
    all_scores = []
    all_mae_histories = []

    for i in range(k):
        # print('processing fold #',i)
        # Prep training data from all other partitions
        val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
        val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

        partial_train_data = np.concatenate([train_data[:i * num_val_samples], train_data[(i + 1) * num_val_samples:]], axis=0)
        partial_train_targets = np.concatenate([train_targets[:i * num_val_samples], train_targets[(i + 1) * num_val_samples:]], axis=0)

        model = build_model(train_data)
        history = model.fit(partial_train_data, partial_train_targets, epochs=num_epochs, batch_size=1, verbose=0)
        mae_history = history.history['mae']
        val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)
        all_scores.append(val_mae)
        all_mae_histories.append(mae_history)

    # Plot error to evalute the model
    # average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]
    # smooth_mae_history = smooth_curve(average_mae_history)
    # print("AVERAGE MAE HISTORY: "+str(average_mae_history))


    # plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
    # plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
    # plt.xlabel('Epochs')
    # plt.ylabel('Smoothed Validation MAE')
    # plt.show()

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")
