from flask import Flask, jsonify, render_template

from simulation import simulation


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/state")
def get_state():

    return jsonify(
        simulation.get_state()
    )


@app.route("/api/step", methods=["POST"])
def step_simulation():

    simulation.step_simulation()

    return jsonify(
        simulation.get_state()
    )


@app.route("/api/start", methods=["POST"])
def start_simulation():

    simulation.start()

    return jsonify(
        simulation.get_state()
    )


@app.route("/api/stop", methods=["POST"])
def stop_simulation():

    simulation.stop()

    return jsonify(
        simulation.get_state()
    )


@app.route("/api/reset", methods=["POST"])
def reset_simulation():

    simulation.reset()

    return jsonify(
        simulation.get_state()
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )