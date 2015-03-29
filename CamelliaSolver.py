import Driver


def main():
    """Here. We. Go."""

	state = initial();
	
	printf("Welcome to the PyCamellia incompressible flow solver!\n");
	state.prompt();
	inputString = raw_input("");

	state = state.parse(inputString);

	
    pass
    #this statement does nothing

Driver.main()

