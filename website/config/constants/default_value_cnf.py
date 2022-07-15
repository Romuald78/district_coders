## models default value
# in second
TIMEOUT_DEFAULT_VALUE = 10

## execution default value
# in bytes
MAX_LENGTH_USER_RAW_CODE = 250000
# in bytes
MAX_MEMORY_USER_CODE = pow(2, 20)  # 1 Mo

# exit code from system (exercice_inspector)
# 0 to 200 means user execution encountered no issues
# but may be not correct from the exercise point of view
# 201 to 255 means error
EX_INSPECT_ERROR_RANGE_MIN = 201
