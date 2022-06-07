# ------------------------
# COMMANDS
# ------------------------
CC    = gcc
MKDIR = mkdir
RMDIR = rm -rf
AR    = ar -rcs

# ------------------------
# DIRECTORIES
# ------------------------
TMP_DIR = tmp
BIN_DIR = bin
USR_DIR = users
LIB_DIR = libDC
EXO_DIR = exercices

# ------------------------
# EXERCICES
# ------------------------
EXO_C = $(wildcard $(EXO_DIR)/*.c)
EXO_O = $(patsubst $(EXO_DIR)/%, $(BIN_DIR)/%, $(EXO_C))
EXO   = $(patsubst %.c, %.exe, $(EXO_O))

# ------------------------
# NAMES
# ------------------------
LIB = DC


$(EXO)/%.exe : $(EXO_C)/%.c
	gcc $< -o $@ -L$(TMP_DIR) -l$(LIB)

$(TMP_DIR)/lib$(LIB).a : $(TMP_DIR)/genDC.o | $(TMP_DIR)
	$(AR) $@ $<

$(TMP_DIR)/genDC.o : $(LIB_DIR)/genDC.c $(LIB_DIR)/genDC.h $(TMP_DIR) | $(TMP_DIR)
	$(CC) -c $< -o $@

$(TMP_DIR) $(BIN_DIR) : 
	$(MKDIR) $@

clean : 
	$(RMDIR) $(TMP_DIR) $(BIN_DIR)

debug:
	@echo $(EXO_C)
	@echo $(EXO_O)
	@echo $(EXO)

