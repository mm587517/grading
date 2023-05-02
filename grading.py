import inquirer
import json
import pyperclip as pc

# Define the filename to save the grading sections to
file_name = "grading_sections.json"

# Load any previously saved grading sections from the file
try:
    with open(file_name, "r") as f:
        grading_sections_map = json.load(f)
except FileNotFoundError:
    grading_sections_map = {}


# Define a function to prompt the user for a new section
def prompt_for_section():
    questions = [inquirer.Text("name", message="Enter the name of the new section:")]
    answers = inquirer.prompt(questions)
    return answers["name"]


# Define a function to prompt the user for the point value of a new section
def prompt_for_point_value(section_name):
    questions = [
        inquirer.List(
            "points",
            message=f"How many points is {section_name} worth?",
            choices=list(range(1, 101)),
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["points"]


# Define a function to prompt the user for a point deduction for a section
def prompt_for_deduction(section_name):
    questions = [
        inquirer.List(
            "deduction",
            message=f"How many points do you want to deduct from {section_name}?",
            choices=list(range(0, grading_sections_map[section_name] + 1)),
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["deduction"]


# Define a function to perform the grading
def perform_grading():
    # Prompt the user to add as many grading sections as they want
    while True:
        add_section_question = inquirer.Confirm(
            "add_section", message="Do you want to add a new grading section?"
        )
        add_section_answer = inquirer.prompt([add_section_question])

        if not add_section_answer["add_section"]:
            break

        section_name = prompt_for_section()
        section_points = prompt_for_point_value(section_name)
        grading_sections_map[section_name] = section_points

    # Write the grading sections map to the file
    with open(file_name, "w") as f:
        json.dump(grading_sections_map, f)

    # Iterate through the grading sections and prompt the user for a deduction for each one
    results = []
    total_points = 0
    max_points = 0
    for section_name, section_points in grading_sections_map.items():
        deduction = prompt_for_deduction(section_name)
        section_points = section_points - deduction
        total_points += section_points
        max_points += section_points + deduction
        result_str = f"-{deduction} points for {section_name}"
        results.append(result_str)
        print(
            f"{section_name}: {section_points}/{grading_sections_map[section_name]} ({result_str})"
        )

    # Copy the grading results to the clipboard
    results_str = "\n".join(results)
    total_score_str = f"Total Score: {total_points}/{max_points}"
    pc.copy(f"{results_str}\n{total_score_str}")
    print(f"\n{total_score_str}")
    print(f"\nGrading Results copied to clipboard:\n{results_str}")


# Define a function to ask the user if they want to keep grading
def ask_to_continue():
    questions = [
        inquirer.Confirm("keep_grading", message="Do you want to keep grading?")
    ]
    answers = inquirer.prompt(questions)
    return answers["keep_grading"]


# Perform the grading as many times as the user wants
while True:
    perform_grading()
    if not ask_to_continue():
        break
    grading_sections_map = {}

print("Grading complete. Exiting.")
