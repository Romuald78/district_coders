# ERROR_CONST = ["the status", "the error details"]
## ERROR MESSAGE (for exit_code)

# User permission (groups)
GROUP_PERMISSION_ASSESSMENT = ["Not available", "None of your groups can access to this assessment"]
GROUP_PERMISSION_EXERCISE   = ["Not available", "None of your groups can access to this exercise"  ]

# User permission (dates)
DATE_PERMISSION_FUTURE            = ["Not available yet", "Future assessments aren't accessible"]
DATE_PERMISSION_PAST_NOT_TRAINING = ["Not available yet", "You cannot access to this exercise yet"]
DATE_PERMISSION_IN_PROCESS        = ["", "This exercise is available in another assessment"]

# Exercice resolving
COMPILE_ERROR = ["GCC compilation", "Error during compilation phase"]

# User permission (rank)
RANK_PERMISSION_TOO_HIGH = ["Locked", "Please complete lower rank exercise"]

# User permission (exercise complete)
RANK_PERMISSION_COMPLETE = ["Done", "You cannot retry a solved exercise"]

# User permission (language)
LANGUAGE_NOT_AVAILABLE = ["Unavailable language", "The language is not available for this exercise"]

# item not found
ASSESSMENT_NOT_FOUNT   = ["Unknown", "Unable to find the assessment"]
EXERCISE_NOT_FOUND     = ["Unknown", "Unable to find the exercise"]
EXOTEST2LANG_NOT_FOUND = ["Unknown", "Unable to find the exercise"]

# USER RAW CODE
USER_RAW_CODE_TOO_BIG = ["Too many characters", "Your code contains too many characters"]

# groups register
GROUP_REGISTER_EMPTY_KEY   = ["Unknown", "Please enter a valid group key"]
GROUP_REGISTER_INVALID_KEY = ["Unvalide key", "Group not found"]
GROUP_REGISTER_ALREADY_IN  = ["Already in", "You are already in this group"]

# TestResult
TESTRESULT_NOT_FOUND = ["Unknown", "Unable to find a valid TestResult"]

# General
UNKNOWN_ERROR    = ["Unknown", "What ? I mean, I don't know what is happening"]
FEATURE_NOT_BUG  = ["Working", "It's a feature, not a bug"]
IN_BUILDING_PAGE = ["Not finished", "Be patient, the site is not totally finished yet"]

# EMAIL CONFIRMATION
EMAIL_INVALID         = ["Invalid Email", "Please enter a valid email address"]
EMAIL_CONFIRM_ERROR   = ["Email not confirmed", "We're sorry, we haven't be able to confirm your email, please try again"]
EMAIL_ALREADY_CONFIRM = ["Email already confirmed", "You already confirm your email. You can login now"]

# PASSWORD
PASSWORD_INVALID = ["Invalid password", "Please enter a valid password"]

# LANGUAGE PROGRAM NOT SUPPORTED
LANGUAGE_NOT_SUPPORTED = ["Unsupported language", "The language given is not supported"]

# Exit code to return from exercise controllers / inspector (python side)
ERROR_CODE_OK          = 0
ERROR_CODE_ACCESS      = -3
ERROR_CODE_NOT_FOUND   = -4
ERROR_CODE_TIMEOUT     = -8
ERROR_CODE_CONFLICT    = -9
ERROR_CODE_PARAMS      = -12
ERROR_CODE_UNSUPPORTED = -15
ERROR_CODE_IMPOSSIBLE  = -18
ERROR_CODE_COMPILE     = -22

