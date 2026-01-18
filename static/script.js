// script.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("plannerForm");
    const workoutOutput = document.querySelector("#workoutPlan pre");
    const dietOutput = document.querySelector("#dietPlan pre");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Gather form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            // Convert some inputs to proper types
            if (["weight", "height", "age", "bodyfat"].includes(key)) {
                data[key] = parseFloat(value);
            } else if (key === "gym") {
                data[key] = value === "true"; // boolean
            } else {
                data[key] = value;
            }
        });

        // Clear previous output
        workoutOutput.textContent = "Generating...";
        dietOutput.textContent = "Generating...";

        try {
            // Call backend
            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error("Failed to fetch plan");

            const result = await response.json();

            // Display output
            workoutOutput.textContent = result.workout;
            dietOutput.textContent = result.diet;
        } catch (error) {
            workoutOutput.textContent = "Error generating plan.";
            dietOutput.textContent = "Error generating plan.";
            console.error(error);
        }
    });
});
