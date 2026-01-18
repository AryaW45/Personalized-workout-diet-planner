import random
import math

# Refactored logic.py
# - Maintains original generate_plan(data) signature and string outputs
# - Scientific workout splitting (based on fitness level)
# - Macro calculations: protein 1.6-2.2 g/kg, fats 20-30% of calories, carbs = remainder
# - Meal-level macro distribution more evidence-aligned
# - Keeps food_map and workouts data structure compatible with other files

# ======================
# === Workouts Data ===
# (kept the original lists for compatibility)
# ======================

gym_workouts = {
    "legs": [
        "Squat — Quads/Glutes",
        "Front Squat — Quads",
        "Bulgarian Split Squat — Quads/Glutes",
        "Leg Press — Quads/Glutes",
        "Walking Lunges — Quads/Glutes",
        "Romanian Deadlift (RDL) — Hamstrings/Glutes",
        "Hip Thrust — Glutes",
        "Glute Kickback (Cable) — Glutes",
        "Leg Curl (Machine) — Hamstrings",
        "Calf Raise (Standing/Seated) — Calves"
    ],
    "chest": [
        "Bench Press (Barbell) — Chest",
        "Incline Dumbbell Press — Upper Chest",
        "Decline Press — Lower Chest",
        "Chest Fly (Dumbbell or Cable) — Chest",
        "Pushups (Weighted or Machine Assist) — Chest/Triceps"
    ],
    "back": [
        "Deadlift — Back/Glutes",
        "Lat Pulldown — Lats",
        "Pull-ups/Chin-ups — Lats/Biceps",
        "Seated Cable Row — Mid Back",
        "Barbell Row — Mid Back",
        "T-Bar Row — Mid Back",
        "Face Pulls — Rear Delts/Traps"
    ],
    "shoulders": [
        "Overhead Press (Barbell or Dumbbell) — Shoulders",
        "Arnold Press — Shoulders",
        "Lateral Raise — Side Delts",
        "Front Raise — Front Delts",
        "Rear Delt Fly — Rear Delts"
    ],
    "arms": [
        "Bicep Curl (Dumbbell/Barbell) — Biceps",
        "Hammer Curl — Biceps/Forearms",
        "Tricep Pushdown (Cable) — Triceps",
        "Skull Crushers (EZ Bar) — Triceps",
        "Dips (Weighted) — Triceps/Chest"
    ],
    "core": [
        "Plank (Weighted or Machine) — Core",
        "Hanging Leg Raise — Lower Abs",
        "Cable Crunch — Abs",
        "Ab Wheel Rollout — Core",
        "Russian Twists (with Weight) — Obliques"
    ],
    "fullbody": [
        "Clean and Press — Full Body",
        "Kettlebell Swing — Posterior Chain",
        "Farmer’s Carry — Core/Grip/Legs"
    ]
}

home_workouts = {
    "legs": [
        "Bodyweight Squats — Quads/Glutes",
        "Jump Squats — Quads/Glutes/Cardio",
        "Split Squats — Quads/Glutes",
        "Bulgarian Split Squats (using a chair) — Quads/Glutes",
        "Lunges (Forward/Reverse/Walking) — Quads/Glutes",
        "Step-ups (onto a chair/bench) — Quads/Glutes",
        "Glute Bridge — Glutes",
        "Hip Thrust (against couch/bed) — Glutes",
        "Wall Sit — Quads",
        "Calf Raises — Calves"
    ],
    "chest": [
        "Pushups (Standard) — Chest/Triceps",
        "Incline Pushups (hands elevated) — Chest",
        "Decline Pushups (feet elevated) — Chest",
        "Diamond Pushups — Chest/Triceps",
        "Wide Pushups — Chest",
        "Pike Pushups — Shoulders/Chest",
        "Hindu Pushups — Chest/Shoulders"
    ],
    "back": [
        "Superman Hold — Lower Back",
        "Reverse Snow Angels — Upper Back",
        "Prone Y-T-W Raises — Rear Delts/Traps",
        "Resistance Band Rows — Lats/Mid Back",
        "Towel Rows (under table) — Lats/Biceps"
    ],
    "shoulders": [
        "Shoulder Taps (from plank) — Shoulders/Core",
        "Arm Circles (dynamic) — Shoulders",
        "Tricep Dips (on chair/bench) — Triceps",
        "Inverted Pushups (pike position) — Shoulders",
        "Bicep Curls with Backpack/Water Bottles — Biceps",
        "Lateral Raises with Backpack/Water Bottles — Shoulders"
    ],
    "core": [
        "Plank (Standard, Side, Shoulder Tap) — Core",
        "Mountain Climbers — Core/Cardio",
        "Leg Raises — Lower Abs",
        "Flutter Kicks — Lower Abs",
        "Bicycle Crunches — Obliques",
        "Russian Twists (weighted/unweighted) — Obliques",
        "Hollow Body Hold — Core",
        "Bird Dog — Core/Stability",
        "Dead Bug — Core/Stability",
        "Side Plank — Obliques"
    ],
    "fullbody": [
        "Burpees — Full Body/Cardio",
        "Jumping Jacks — Full Body/Cardio",
        "High Knees — Cardio",
        "Skater Jumps — Legs/Cardio",
        "Bear Crawls — Core/Shoulders",
        "Crab Walk — Core/Shoulders/Glutes"
    ]
}

# ======================
# === Food Data ===
# ======================

food_map = {
    "omnivore": {
        "protein": [
            "Chicken breast", "Chicken thigh", "Salmon", "White fish",
            "Prawns", "Eggs", "Egg whites", "Greek yogurt",
            "Skim milk", "Cottage cheese", "Paneer", "Turkey breast",
            "Lean beef", "Lamb", "Tofu", "Tempeh", "Soy chunks",
            "Whey protein", "Lentils", "Chickpeas"
        ],
        "carbs": [
            "Brown rice", "White rice", "Quinoa", "Oats",
            "Sweet potato", "Potato", "Whole wheat bread", "Chapati",
            "Pasta", "Couscous", "Corn", "Banana",
            "Apple", "Orange", "Berries", "Dates", "Honey",
            "Daliya", "Rajma", "Chole"
        ],
        "fats": [
            "Olive oil", "Ghee", "Almonds", "Walnuts", "Cashews",
            "Peanuts", "Peanut butter", "Avocado", "Chia seeds", "Flaxseeds",
            "Pumpkin seeds", "Sunflower seeds", "Coconut", "Dark chocolate",
            "Tahini"
        ]
    },
    "vegetarian": {
        "protein": [
            "Paneer", "Cottage cheese", "Tofu", "Tempeh", "Soy chunks",
            "Lentils", "Dal", "Chickpeas", "Rajma",
            "Moong beans", "Black beans", "Kidney beans",
            "Peas", "Quark/curd", "Skim milk", "Buttermilk",
            "Eggs", "Whey protein", "Edamame", "Sprouts"
        ],
        "carbs": [
            "Rice", "Brown rice", "Quinoa", "Oats",
            "Daliya", "Poha", "Idli", "Dosa",
            "Chapati", "Whole wheat bread", "Sweet potato",
            "Potato", "Corn", "Fruits", "Dry fruits", "Vegetables"
        ],
        "fats": [
            "Ghee", "Butter", "Almonds", "Walnuts", "Cashews",
            "Pistachios", "Peanuts", "Peanut butter", "Chia seeds", "Flaxseeds",
            "Pumpkin seeds", "Sesame seeds", "Avocado", "Coconut", "Olive oil"
        ]
    },
    "vegan": {
        "protein": [
            "Tofu", "Tempeh", "Soy chunks", "Seitan", "Lentils",
            "Chickpeas", "Kidney beans", "Black beans",
            "Pinto beans", "Edamame", "Green peas", "Pea protein powder",
            "Hemp protein powder", "Chia seeds", "Quinoa", "Oats",
            "Sprouts", "Peanut butter", "Almond butter", "Nutritional yeast"
        ],
        "carbs": [
            "Rice", "Brown rice", "Quinoa", "Oats",
            "Sweet potato", "Potato", "Couscous", "Whole wheat bread",
            "Chapati", "Fruits", "Vegetables", "Corn",
            "Millet", "Daliya", "Rice noodles", "Dates", "Raisins"
        ],
        "fats": [
            "Olive oil", "Coconut oil", "Avocado", "Almonds", "Walnuts",
            "Cashews", "Pistachios", "Peanuts", "Chia seeds", "Flaxseeds",
            "Pumpkin seeds", "Sunflower seeds", "Hemp seeds", "Tahini",
            "Coconut", "Dark chocolate"
        ]
    }
}

# ----------------------
# === Helpers ======
# ----------------------

def _bmr(weight, height, age, gender):
    # Mifflin-St Jeor Equation
    return 10 * weight + 6.25 * height - 5 * age + (5 if gender == "male" else -161)


def _activity_multiplier(activity):
    # Slightly expanded mapping
    mapping = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return mapping.get(activity, 1.4)


def _protein_per_kg(goals, bodyfat, fitness_level):
    # Scientific guideline: 1.6 - 2.2 g/kg depending on goal & level
    base = 1.6
    if "muscle" in goals:
        base = 1.8
    if "fatloss" in goals:
        base = 2.0
    if fitness_level == "advanced":
        base += 0.1
    # If very high bodyfat, we can use absolute protein but keep within 2.2
    return min(2.2, base)


def _fats_calorie_ratio(bodyfat):
    # Use 20-30% calories from fat; if high BF we can keep fat slightly lower
    if bodyfat >= 30:
        return 0.22
    if bodyfat >= 20:
        return 0.25
    return 0.27


def _clamp(value, low, high):
    return max(low, min(high, value))


# ----------------------
# === Workout Builders ===
# ----------------------

def _build_split(fitness_level, gym):
    # Choose a scientifically balanced split based on level
    if fitness_level == "beginner":
        # 3x full body
        return ["fullbody"] * 3
    if fitness_level == "intermediate":
        # 4 day upper/lower split
        return ["upper", "lower", "upper", "lower"]
    # advanced -> 5 day push/pull/legs + upper accessory
    return ["push", "pull", "legs", "upper", "accessory"]


def _select_exercises_for_day(day_type, selected_workouts, gym):
    # Map day_type to targeted groups
    mapping = {
        "fullbody": ["fullbody", "legs", "back", "chest", "shoulders", "core"],
        "upper": ["chest", "back", "shoulders", "arms", "core"],
        "lower": ["legs", "core"],
        "push": ["chest", "shoulders", "arms", "core"],
        "pull": ["back", "arms", "core"],
        "legs": ["legs", "core"],
        "accessory": ["chest", "back", "shoulders", "core"]
    }

    groups = mapping.get(day_type, ["fullbody"])
    day_exercises = []

    # pick 1-2 compound + 1-2 accessory per main group
    for group in groups:
        exercises = selected_workouts.get(group, [])
        if not exercises:
            continue
        # compounds preference: prefer multi-joint names
        compounds = [e for e in exercises if any(k in e.lower() for k in ["squat", "deadlift", "press", "row", "clean", "thrust", "dip"]) ]
        accessories = [e for e in exercises if e not in compounds]

        picks = []
        if compounds:
            picks.append(random.choice(compounds))
        if accessories and random.random() < 0.7:
            picks.append(random.choice(accessories))

        # limit per group to 2 picks
        picks = picks[:2]

        # decide sets/reps based on compound vs accessory
        for ex in picks:
            if any(k in ex.lower() for k in ["squat", "deadlift", "clean", "press", "row"]):
                sets = random.choice([3,4])
                reps = random.choice([5,6,8,10])
            else:
                sets = random.choice([3,4])
                reps = random.choice([8,10,12,15])
            day_exercises.append((ex, sets, reps))

    # Add 1 fullbody accessory occasionally for conditioning
    if random.random() < 0.35 and "fullbody" in selected_workouts:
        fb = random.choice(selected_workouts["fullbody"])
        day_exercises.append((fb, 3, random.choice([8,10,12,15])))

    return day_exercises


# ----------------------
# === Diet Builders ===
# ----------------------

# Meal macro distribution (evidence-aligned):
MEAL_MACRO_RATIO = {
    "Breakfast": {"protein": 0.25, "carbs": 0.30, "fats": 0.25},
    "Lunch": {"protein": 0.30, "carbs": 0.35, "fats": 0.30},
    "Dinner": {"protein": 0.30, "carbs": 0.30, "fats": 0.30},
    "Snack": {"protein": 0.15, "carbs": 0.05, "fats": 0.15}
}


def _pick_foods_for_meal(foods, meal, include_fat=True):
    # Return a short string listing 2-3 foods per meal (keeps compatibility)
    parts = []
    # always include a protein source
    parts.append(random.choice(foods["protein"]))
    # include a carb if meal expects carbs > small
    if MEAL_MACRO_RATIO[meal]["carbs"] > 0.08:
        parts.append(random.choice(foods["carbs"]))
    # include fat sometimes
    if include_fat and MEAL_MACRO_RATIO[meal]["fats"] > 0.18:
        parts.append(random.choice(foods["fats"]))
    return " + ".join(parts)


# ----------------------
# === Public API ======
# ----------------------

def generate_plan(data):
    """Generates (workout_plan_str, diet_plan_str) given input data dict.
    Keeps the return types compatible with the original project.

    Expected keys in data: weight(kg), height(cm), age, gender ("male"/"female"),
    gym (bool), bodyfat (%), activity (one of activity mapping keys),
    fitness_level ("beginner"/"intermediate"/"advanced"), diet_type (omnivore/vegetarian/vegan),
    goals (list or set of strings containing 'muscle','fatloss','recomp')
    """

    # --- 1. Read inputs ---
    weight = float(data.get("weight", 70))
    height = float(data.get("height", 175))
    age = int(data.get("age", 30))
    gender = data.get("gender", "male").lower()
    gym = bool(data.get("gym", True))
    bodyfat = float(data.get("bodyfat", 20))
    activity = data.get("activity", "moderate")
    fitness_level = data.get("fitness_level", "intermediate")
    diet_type = data.get("diet_type", "omnivore")
    goals = data.get("goals", [])
    if isinstance(goals, str):
        goals = [goals]

    # --- 2. Calories ---
    bmr = _bmr(weight, height, age, gender)
    activity_mult = _activity_multiplier(activity)
    tdee = bmr * activity_mult

    # goal adjustments: muscle +15%, fatloss -20%, recomp slight +5%
    goal_adj = 0.0
    if "muscle" in goals:
        goal_adj += 0.15
    if "fatloss" in goals:
        goal_adj -= 0.20
    if "recomp" in goals:
        goal_adj += 0.05

    calories = int(round(tdee * (1 + goal_adj)))

    # enforce realistic calorie bounds to avoid absurd low/high outputs
    calories = int(_clamp(calories, 1200, 6000))

    # --- 3. Macros ---
    prot_g_per_kg = _protein_per_kg(goals, bodyfat, fitness_level)
    protein = int(round(weight * prot_g_per_kg))

    fat_ratio = _fats_calorie_ratio(bodyfat)
    fats_cal = int(round(calories * fat_ratio))
    fats = int(round(fats_cal / 9.0))

    # carbs are remaining calories
    carbs_cal = calories - (protein * 4 + fats * 9)
    carbs = int(round(max(0, carbs_cal / 4.0)))

    # safety clamps: ensure macros not extreme
    protein = int(_clamp(protein, int(weight * 1.2), int(weight * 2.2)))
    fats = int(_clamp(fats, 20, int(weight * 1.5)))
    carbs = int(_clamp(carbs, 0, 1000))

    # --- 4. Workout Plan ---
    plan_days = {"beginner": 3, "intermediate": 4, "advanced": 5}.get(fitness_level, 4)
    selected_workouts = gym_workouts if gym else home_workouts

    split = _build_split(fitness_level, gym)
    # ensure split length equals plan_days
    split = split[:plan_days]

    workout_plan = ""
    for i, day_type in enumerate(split):
        day_exs = _select_exercises_for_day(day_type, selected_workouts, gym)
        workout_plan += f"Day {i+1}:\n"
        for ex, sets, reps in day_exs:
            workout_plan += f"- {ex}: {sets} sets x {reps} reps\n"
        workout_plan += "\n"

    # --- 5. Diet Plan ---
    foods = food_map.get(diet_type, food_map["omnivore"])
    meals = ["Breakfast", "Lunch", "Dinner", "Snack"]

    diet_plan = ""
    for meal in meals:
        if meal == "Snack":
            diet_plan += f"{meal}: {_pick_foods_for_meal(foods, meal, include_fat=False)}\n"
        else:
            diet_plan += f"{meal}: {_pick_foods_for_meal(foods, meal)}\n"

    diet_plan += (
        f"\nTarget Range: {int(calories*0.95)}-{int(calories*1.05)} kcal — "
        f"Protein: {int(protein*0.95)}-{int(protein*1.05)}g, "
        f"Carbs: {int(carbs*0.95)}-{int(carbs*1.05)}g, "
        f"Fats: {int(fats*0.95)}-{int(fats*1.05)}g\n"
    )

    return workout_plan.strip(), diet_plan.strip()
