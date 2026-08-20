import sys
import vtk


def add_scalar_fields(mesh, functions):
    """
    Add scalar fields to the mesh.

    functions:
        Dictionary mapping field names to functions of (x, y, z).

        Example:
            {
                "f1": lambda x, y, z: x,
                "f2": lambda x, y, z: x * x,
            }
    """

    for name, function in functions.items():

        field = vtk.vtkDoubleArray()
        field.SetName(name)
        field.SetNumberOfComponents(1)
        field.SetNumberOfTuples(mesh.GetNumberOfPoints())

        for i in range(mesh.GetNumberOfPoints()):

            x, y, z = mesh.GetPoint(i)

            field.SetValue(i, function(x, y, z))

        mesh.GetPointData().AddArray(field)


def generate_vtu(output_file, resolution, functions):

    # Create 5x5x5 grid
    image = vtk.vtkImageData()
    image.SetDimensions(resolution, resolution, resolution)
    image.SetOrigin(0.0, 0.0, 0.0)
    image.SetSpacing(1.0, 1.0, 1.0)

    # Tetrahedralize
    tetra = vtk.vtkDataSetTriangleFilter()
    tetra.SetInputData(image)
    tetra.Update()

    mesh = tetra.GetOutput()

    # Add requested scalar fields
    add_scalar_fields(mesh, functions)

    # Write VTU
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(mesh)
    writer.Write()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output.vtu>")
        sys.exit(1)

    functions = {
        "f1": lambda x, y, z: x,
        "f2": lambda x, y, z: x * x,
    }

    generate_vtu(sys.argv[1], 5, functions)
