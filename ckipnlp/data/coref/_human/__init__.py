from ._alumnus import ALUMNUS_WORDS
from ._aristocrat import ARISTOCRAT_WORDS
from ._candidate import CANDIDATE_WORDS
from ._fans import FANS_WORDS
from ._humanized import HUMANIZED_WORDS
from ._member import MEMBER_WORDS
from ._owner import OWNER_WORDS
from ._professional import PROFESSIONAL_WORDS
from ._recipient import RECIPIENT_WORDS
from ._religious_follower import RELIGIOUS_FOLLOWER_WORDS
from ._sage import SAGE_WORDS
from ._sick_patient import SICK_PATIENT_WORDS
from ._student import STUDENT_WORDS
from ._talent import TALENT_WORDS
from ._victim import VICTIM_WORDS
from ._warrior import WARRIOR_WORDS

from ._instance import HUMAN_INSTANCE_WORDS

HUMAN_WORDS = {
    *ALUMNUS_WORDS,
    *ARISTOCRAT_WORDS,
    *CANDIDATE_WORDS,
    *FANS_WORDS,
    *HUMANIZED_WORDS,
    *MEMBER_WORDS,
    *OWNER_WORDS,
    *PROFESSIONAL_WORDS,
    *RECIPIENT_WORDS,
    *RELIGIOUS_FOLLOWER_WORDS,
    *SAGE_WORDS,
    *SICK_PATIENT_WORDS,
    *STUDENT_WORDS,
    *TALENT_WORDS,
    *VICTIM_WORDS,
    *WARRIOR_WORDS,

    *HUMAN_INSTANCE_WORDS,
}
