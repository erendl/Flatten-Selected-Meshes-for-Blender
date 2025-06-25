# Flatten Selected Meshes for Blender

A simple Blender add-on that flattens imported GLB hierarchies by joining selected mesh objects into a single mesh and cleaning up unused parents and collections.

## Features

- Joins only selected mesh objects into one (e.g. model_1, model_2, ...)
- Clears parent relationships (e.g. GLTF_SceneRootNode, Empty)
- Removes unused parent objects and empty collections
- Avoids merging previously flattened models

## Installation

1. Download `flatten_selected_meshes.zip`
2. In Blender, go to `Edit > Preferences > Add-ons > Install`
4. Press `N` in the 3D Viewport and go to the **Flatten** tab

## Usage

1. Import your GLB model(s)
2. Select the mesh objects you want to flatten
3. Click **Flatten Selected Meshes (Clean)** in the sidebar

## License

MIT
