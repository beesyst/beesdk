from enum import Enum


class AuthorityLevel(str, Enum):
    READ_ONLY = "read_only"
    DRAFT_ONLY = "draft_only"
    EXECUTION_CAPABLE = "execution_capable"
