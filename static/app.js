let simulationTimer = null;


/* ================================
   GET CURRENT STATE
================================ */

async function getState() {

    const response =
        await fetch("/api/state");

    const state =
        await response.json();

    updateDashboard(state);
}


/* ================================
   UPDATE DASHBOARD
================================ */

function updateDashboard(state) {


    /* ----------------------------
       Robot
    ---------------------------- */

    document.getElementById(
        "robot-state"
    ).textContent =
        state.state;


    document.getElementById(
        "robot-position"
    ).textContent =
        `(${state.position[0]}, ${state.position[1]})`;


    document.getElementById(
        "robot-direction"
    ).textContent =
        state.direction;


    document.getElementById(
        "robot-carrying"
    ).textContent =
        state.carrying || "Nothing";


    /* ----------------------------
       Sensors
    ---------------------------- */

    document.getElementById(
        "sensor-front"
    ).textContent =
        state.sensors.front;


    document.getElementById(
        "sensor-left"
    ).textContent =
        state.sensors.left;


    document.getElementById(
        "sensor-right"
    ).textContent =
        state.sensors.right;


    /* ----------------------------
       Sorting statistics
    ---------------------------- */

    document.getElementById(
        "objects-sorted"
    ).textContent =
        state.statistics.objects_sorted;


    document.getElementById(
        "objects-remaining"
    ).textContent =
        state.objects.remaining;


    document.getElementById(
        "success-rate"
    ).textContent =
        `${state.statistics.success_rate}%`;


    document.getElementById(
        "objects-failed"
    ).textContent =
        state.statistics.objects_failed;


    /* ----------------------------
       Simulation statistics
    ---------------------------- */

    document.getElementById(
        "simulation-step"
    ).textContent =
        state.step;


    document.getElementById(
        "robot-moves"
    ).textContent =
        state.statistics.total_moves;


    document.getElementById(
        "failed-moves"
    ).textContent =
        state.statistics.failed_moves;


    document.getElementById(
        "planned-path-steps"
    ).textContent =
        state.statistics.planned_path_steps;


    /* ----------------------------
       Status
    ---------------------------- */

    let statusText;


    if (state.finished) {

        statusText = "Finished";

    } else if (state.running) {

        statusText = "Running";

    } else {

        statusText = "Stopped";
    }


    document.getElementById(
        "simulation-status"
    ).textContent =
        statusText;


    updateStatusBadge(state);


    updateMap(state);


    updateActivityLog(state);
}


/* ================================
   STATUS BADGE
================================ */

function updateStatusBadge(state) {

    const badge =
        document.getElementById(
            "status-badge"
        );


    const label =
        document.getElementById(
            "header-status"
        );


    badge.classList.remove(
        "running",
        "stopped",
        "finished"
    );


    if (state.finished) {

        badge.classList.add(
            "finished"
        );

        label.textContent =
            "FINISHED";

    } else if (state.running) {

        badge.classList.add(
            "running"
        );

        label.textContent =
            "LIVE";

    } else {

        badge.classList.add(
            "stopped"
        );

        label.textContent =
            "STOPPED";
    }
}


/* ================================
   STEP
================================ */

async function stepSimulation() {

    const response =
        await fetch(
            "/api/step",
            {
                method: "POST"
            }
        );


    const state =
        await response.json();


    updateDashboard(state);


    if (state.finished) {

        stopAutomaticRun();
    }
}


/* ================================
   START
================================ */

async function startSimulation() {

    if (simulationTimer !== null) {
        return;
    }


    const response =
        await fetch(
            "/api/start",
            {
                method: "POST"
            }
        );


    const state =
        await response.json();


    updateDashboard(state);


    simulationTimer =
        setInterval(
            async function () {

                if (
                    simulationTimer === null
                ) {
                    return;
                }


                await stepSimulation();

            },
            400
        );
}


/* ================================
   STOP
================================ */

async function stopSimulation() {

    await fetch(
        "/api/stop",
        {
            method: "POST"
        }
    );


    stopAutomaticRun();


    await getState();
}


/* ================================
   STOP TIMER
================================ */

function stopAutomaticRun() {

    if (
        simulationTimer !== null
    ) {

        clearInterval(
            simulationTimer
        );

        simulationTimer = null;
    }
}


/* ================================
   RESET
================================ */

async function resetSimulation() {

    stopAutomaticRun();


    const response =
        await fetch(
            "/api/reset",
            {
                method: "POST"
            }
        );


    const state =
        await response.json();


    updateDashboard(state);
}


/* ================================
   MAP CELL CONTENT
================================ */

function getCellContent(
    x,
    y,
    state
) {


    /* ----------------------------
       Dynamic obstacle
    ---------------------------- */

    const dynamicObstacle =
        state.environment.dynamic_obstacles.some(
            position =>
                position[0] === x &&
                position[1] === y
        );


    if (dynamicObstacle) {

        return "X";
    }


    /* ----------------------------
       Static obstacle
    ---------------------------- */

    const staticObstacle =
        state.environment.static_obstacles.some(
            position =>
                position[0] === x &&
                position[1] === y
        );


    if (staticObstacle) {

        return "#";
    }


    /* ----------------------------
       Objects
    ---------------------------- */

    const object =
        state.objects.locations.find(
            item =>
                item.position[0] === x &&
                item.position[1] === y
        );


    if (object) {

        return object.type;
    }


    /* ----------------------------
       Zone A
    ---------------------------- */

    const zoneA =
        state.environment.zones.A;


    if (
        x === zoneA[0] &&
        y === zoneA[1]
    ) {

        return "A";
    }


    /* ----------------------------
       Zone B
    ---------------------------- */

    const zoneB =
        state.environment.zones.B;


    if (
        x === zoneB[0] &&
        y === zoneB[1]
    ) {

        return "B";
    }


    return "";
}


/* ================================
   MAP CELL CLASS
================================ */

function getCellClass(
    x,
    y,
    state
) {

    const classes = [
        "map-cell"
    ];


    /* Dynamic obstacle */

    const dynamicObstacle =
        state.environment.dynamic_obstacles.some(
            position =>
                position[0] === x &&
                position[1] === y
        );


    if (dynamicObstacle) {

        classes.push(
            "dynamic-obstacle"
        );

        return classes.join(" ");
    }


    /* Static obstacle */

    const staticObstacle =
        state.environment.static_obstacles.some(
            position =>
                position[0] === x &&
                position[1] === y
        );


    if (staticObstacle) {

        classes.push(
            "static-obstacle"
        );

        return classes.join(" ");
    }


    /* Object */

    const object =
        state.objects.locations.find(
            item =>
                item.position[0] === x &&
                item.position[1] === y
        );


    if (object) {

        if (
            object.type === "A"
        ) {

            classes.push(
                "object-a"
            );

        } else {

            classes.push(
                "object-b"
            );
        }


        return classes.join(" ");
    }


    /* Zone A */

    const zoneA =
        state.environment.zones.A;


    if (
        x === zoneA[0] &&
        y === zoneA[1]
    ) {

        classes.push(
            "zone-a"
        );

        return classes.join(" ");
    }


    /* Zone B */

    const zoneB =
        state.environment.zones.B;


    if (
        x === zoneB[0] &&
        y === zoneB[1]
    ) {

        classes.push(
            "zone-b"
        );

        return classes.join(" ");
    }


    return classes.join(" ");
}


/* ================================
   UPDATE MAP
================================ */

function updateMap(state) {

    const map =
        document.getElementById(
            "map"
        );


    let grid =
        map.querySelector(
            ".robot-map"
        );


    /*
        Create grid only once.
    */

    if (!grid) {

        grid =
            document.createElement(
                "div"
            );


        grid.className =
            "robot-map";


        const width =
            state.environment.width;

        const height =
            state.environment.height;


        for (
            let y = height - 1;
            y >= 0;
            y--
        ) {

            for (
                let x = 0;
                x < width;
                x++
            ) {

                const cell =
                    document.createElement(
                        "div"
                    );


                cell.className =
                    "map-cell";


                cell.dataset.x =
                    x;

                cell.dataset.y =
                    y;


                cell.title =
                    `Position (${x}, ${y})`;


                grid.appendChild(
                    cell
                );
            }
        }


        /*
            Animated robot marker
        */

        const robotMarker =
            document.createElement(
                "div"
            );


        robotMarker.className =
            "robot-marker";


        grid.appendChild(
            robotMarker
        );


        map.innerHTML = "";


        map.appendChild(
            grid
        );
    }


    /*
        Update cells
    */

    const cells =
        grid.querySelectorAll(
            ".map-cell"
        );


    cells.forEach(
        function (cell) {

            const x =
                Number(
                    cell.dataset.x
                );


            const y =
                Number(
                    cell.dataset.y
                );


            cell.className =
                getCellClass(
                    x,
                    y,
                    state
                );


            cell.textContent =
                getCellContent(
                    x,
                    y,
                    state
                );
        }
    );


    /*
        Update robot
    */

    const robotMarker =
        grid.querySelector(
            ".robot-marker"
        );


    const width =
        state.environment.width;

    const height =
        state.environment.height;


    const robotX =
        state.position[0];

    const robotY =
        state.position[1];


    robotMarker.style.left =
        `${(robotX / width) * 100}%`;


    robotMarker.style.bottom =
        `${(robotY / height) * 100}%`;


    /*
        Robot direction
    */

    const arrows = {

        "N": "↑",

        "E": "→",

        "S": "↓",

        "W": "←"
    };


    robotMarker.textContent =
        arrows[state.direction] || "●";


    /*
        Robot carrying state
    */

    if (state.carrying) {

        robotMarker.title =
            `Robot carrying Type ${state.carrying}`;

    } else {

        robotMarker.title =
            "Robot";
    }
}


/* ================================
   ACTIVITY LOG
================================ */

function updateActivityLog(state) {

    const container =
        document.getElementById(
            "activity-log"
        );


    const events =
        state.activity_log || [];


    if (events.length === 0) {

        container.innerHTML = `
            <div class="activity-empty">
                Waiting for simulation activity...
            </div>
        `;

        return;
    }


    container.innerHTML = "";


    /*
        Show newest event first.
    */

    const reversedEvents =
        [...events].reverse();


    reversedEvents.forEach(
        function (event, index) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                index === 0
                    ? "activity-item latest"
                    : "activity-item";


            item.innerHTML = `

                <span class="activity-step">
                    Step ${event.step}
                </span>

                <span class="activity-message">
                    ${event.message}
                </span>

            `;


            container.appendChild(
                item
            );
        }
    );
}


/* ================================
   INITIAL LOAD
================================ */

getState();