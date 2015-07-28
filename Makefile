
SCRIPT_DIR ?= "make_scripts"

# Removes development/build directories that accumulate over time.
clean:
	@$(SCRIPT_DIR)/clean.bash

moof:
	@$(SCRIPT_DIR)/moof.bash
	
# Creates virtual environments for development using the Python executables in $ENV_LIST. 
# Existing environments are recreated.	
venv:
	@$(SCRIPT_DIR)/venv.bash

