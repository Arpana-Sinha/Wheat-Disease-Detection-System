import tensorflow as tf
import numpy as np

def generate_gradcam(backbone, img_array, last_conv_layer_name):

    grad_model = tf.keras.models.Model(
        inputs=backbone.input,
        outputs=[
            backbone.get_layer(last_conv_layer_name).output,
            backbone.output
        ]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)

        class_idx = tf.argmax(tf.reduce_mean(predictions, axis=(1, 2))[0])
        loss = tf.reduce_mean(predictions[:, :, :, class_idx])

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)

    heatmap /= tf.reduce_max(heatmap) + 1e-8

    return heatmap.numpy()
