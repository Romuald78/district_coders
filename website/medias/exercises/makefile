# ------------------------
# COMMANDS
# ------------------------
CC    = gcc
MKDIR = mkdir
RMDIR = rm -rf
AR    = ar -rcs
LIB   = DC

# ------------------------
# DIRECTORIES
# ------------------------
TMP_DIR = tmp
BIN_DIR = bin
LIB_DIR = lib$(LIB)
EXO_DIR = mode_stdio

# ------------------------
# EXERCISE OBJECTS/EXEC
# ------------------------
EXO_C = $(wildcard $(EXO_DIR)/*.c) $(wildcard $(EXO_DIR)/*/*.c)
#EXO_C = $(shell find $(EXO_DIR) -name '*.c')
SUB_BIN = $(patsubst $(EXO_DIR)/%, $(BIN_DIR)/%, $(EXO_C))
SUB_BIN:= $(sort $(dir $(SUB_BIN)))

EXO_O = $(patsubst $(EXO_DIR)/%, $(TMP_DIR)/%, $(EXO_C))
EXO_O:= $(patsubst %.c, %.o, $(EXO_O))
EXO_X = $(patsubst $(EXO_DIR)/%, $(BIN_DIR)/%, $(EXO_C))
EXO_X:= $(patsubst %.c, %.exe, $(EXO_X))

# ------------------------
# Default target : all executables 
# ------------------------
all : $(EXO_X)
    
# ------------------------
# Process each exercise 
# ------------------------
$(BIN_DIR)/%.exe : $(EXO_DIR)/%.c $(BIN_DIR)/lib$(LIB).a 
	@echo "Generating [`basename $@`] ..."
	@$(CC) $< -o $@ -I$(LIB_DIR) -L$(BIN_DIR) -l$(LIB)

# ------------------------
# Exercise generation lib
# ------------------------
$(BIN_DIR)/lib$(LIB).a : $(LIB_DIR)/genDC.c | $(TMP_DIR) $(BIN_DIR)
	@echo "Generating [lib$(LIB)] ..."
	@$(CC) -c $< -o $(TMP_DIR)/genDC.o
	@$(AR) $@ $(TMP_DIR)/genDC.o

# ------------------------
# Directories + Clean
# ------------------------
$(TMP_DIR) :
	@echo "Creating 'tmp' directory..."
	@$(MKDIR) $@

$(BIN_DIR) :
	@echo "Creating 'bin' directory..."
#	@$(MKDIR) $@
	@$(MKDIR) $(SUB_BIN)

clean : 
	@echo "Removing 'bin' directory..."
	@$(RMDIR) $(BIN_DIR)
	@echo "Removing 'tmp' directory..."
	@$(RMDIR) $(TMP_DIR)

debug:
	@echo $(EXO_C)
	@echo $(SUB_BIN)
	
