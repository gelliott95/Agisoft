# Agisoft

The purpose of the batch process script is to automate the workflow of gradual selection, build dense (point) cloud, classify ground points, build DEM, and build ortho. The batch will then export a report, ortho, and dense cloud in the project's CRS. The title of each item will match the name of the Agisoft project with -report, -ortho, -points appended to the end. All products will be saved in the directory where the Agisoft project is saved.
