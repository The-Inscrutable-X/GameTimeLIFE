### Project Overview: gametimeLIFE

#### Description

The `gametimeLIFE` project is a Python-based application that aims to gamify life experiences and tasks. It uses a tree-like data structure to organize various life categories and their corresponding tasks or events. The project leverages the PySimpleGUI library to provide a basic graphical user interface (GUI) for user interaction. The tree structure is stored in JSON format, allowing for easy saving and loading of user data.

#### Features

- Hierarchical categorization of life experiences and tasks.
- Experience points (XP) associated with each category and task.
- A GUI for creating and managing events.
- Ability to save and load the tree structure in JSON format.

#### Modules

1. **Main Script**: Handles the GUI and the core logic for creating and managing events.
2. **Tree Module**: Contains the `GXP` class for creating and managing the tree structure.

#### Dependencies

- PySimpleGUI
- JSON (Standard Python Library)
- weakref (Standard Python Library)

---

#### Installation

1. Clone the repository.
2. Install the required Python packages.

```bash
pip install PySimpleGUI
```

#### Usage

1. Run the main script to launch the GUI.
2. Create an event by filling in the event name, category, and XP.
3. Click 'Ok' to add the event to the tree structure.

#### Code Structure

- `GXP` Class: General Experience Points class that forms the nodes of the tree.
  - Methods:
    - `insert`: Adds child nodes.
    - `find`: Searches for a node by name.
    - `get_stacked_xp`: Calculates the total XP for a node and its children.
    - `save`: Saves the tree to a JSON file.
- `Task` Class: Inherits from `GXP`, specialized for tasks.
- `load_json_tree`: Function to load the tree from a JSON file.
- `print_xp_tree`: Function to print the tree structure in a readable format.

#### Future Work

- Implement task deadlines and reminders.
- Enhance the GUI for better user experience.
- Add more features like task prioritization.

---

### Technical Insights

The project uses a custom tree data structure implemented through the `GXP` class. Each node in the tree represents a category or a task and holds experience points (XP). The tree is traversable, and each node knows its parent and children, allowing for easy manipulation and data propagation.

The GUI is quite straightforward, built using PySimpleGUI. It allows the user to create new nodes (categories or tasks) and associate them with XP. The tree is displayed in the GUI, giving the user a visual representation of their life categories and tasks.

Error handling is in place to catch invalid entries, and the tree structure can be saved and loaded using JSON serialization.

The project also includes a `Task` class that inherits from `GXP` but adds additional attributes specific to tasks, although it's not fully implemented yet.

`gametimeLIFE` serves as a foundational framework for gamifying life tasks and experiences, offering avenues for further development and feature enhancement.
