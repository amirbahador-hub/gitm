import re
from dataclasses import dataclass
import sqlite3
import sys
# from db import migrate


@dataclass
class Pattern:
    regex: str
    emoji: str
    description: str

def contain_words(*args):
    regex = ""
    for arg in args:
        regex += f"(?=.*(?i){arg})"
    return f"{regex}.*$"

def case_insensetive(word):
    return f"(?i){word}"

patterns = [
        # DEPOY
        Pattern(regex=case_insensetive("deploy"), emoji=":rocket:", description="Deploy stuff."),
        Pattern(regex=contain_words("fix","ci"), emoji=":green_heart:", description="Fix CI Build."),
        Pattern(regex=contain_words("build","ci"), emoji=":construction_worker:", description="Add or update CI build system."),
        Pattern(regex=contain_words("add","ci"), emoji=":construction_worker:", description="Add or update CI build system."),
        Pattern(regex=case_insensetive("release"), emoji=":bookmark:", description="Release / Version tags."),
        Pattern(regex=case_insensetive("merge"), emoji=":twisted_rightwards_arrows:", description="Merge branches."),
        Pattern(regex=case_insensetive("package"), emoji=":package:", description="Add or update compiled files or packages."),
        # DEPENDENCY
        Pattern(regex=contain_words("add","dependencies"), emoji=":heavy_plus_sign:", description="Add a dependency."),
        Pattern(regex=contain_words("add","dependency"), emoji=":heavy_plus_sign:", description="Add a dependency."),
        Pattern(regex=contain_words("remove","dependencies"), emoji=":heavy_minus_sign:", description="Remove a dependency."),
        Pattern(regex=contain_words("remove","dependency"), emoji=":heavy_plus_sign:", description="Remove a dependency."),
        Pattern(regex=contain_words("Down","dependencies"), emoji=":arrow_down:", description="Downgrade dependencies."),
        Pattern(regex=contain_words("Down","dependency"), emoji=":arrow_down:", description="Downgrade dependencies."),
        Pattern(regex=contain_words("Up","dependencies"), emoji=":arrow_up:", description="Upgrade dependencies."),
        Pattern(regex=contain_words("Up","dependency"), emoji=":arrow_up:", description="Upgrade dependencies."),
        Pattern(regex=contain_words("Pin","dependencies"), emoji=":pushpin:", description="Pin dependencies to specific versions."),
        Pattern(regex=contain_words("Pin","dependency"), emoji=":pushpin:", description="Pin dependencies to specific versions."),
        # Common
        Pattern(regex=case_insensetive("rename"), emoji=":truck:", description="Move or rename resources (e.g.: files, paths, routes)."),
        Pattern(regex=case_insensetive("progress"), emoji=":construction:", description="Work in progress."),
        Pattern(regex=contain_words("add","conf"), emoji=":wrench:", description="Add or update configuration files."),
        Pattern(regex=contain_words("update","conf"), emoji=":wrench:", description="Add or update configuration files."),
        Pattern(regex=contain_words("logic","business"), emoji=":necktie:", description="Add or update business logic."),
        Pattern(regex=contain_words("add", "type"), emoji=":label:", description="Add or update types."),
        Pattern(regex=case_insensetive("database"), emoji=":card_file_box:", description="Perform database related changes."),
        Pattern(regex=case_insensetive("multithreading"), emoji=":thread:", description="Add or update code related to multithreading or concurrency."),
        Pattern(regex=case_insensetive("concurrency"), emoji=":thread:", description="Add or update code related to multithreading or concurrency."),
        Pattern(regex=case_insensetive("validation"), emoji=":safety_vest:", description="Add or update code related to validation."),
        Pattern(regex=case_insensetive("translate"), emoji=":globe_with_meridians:", description="Internationalization and localization."),
        Pattern(regex=case_insensetive("Infrastructure"), emoji=":bricks:", description="Infrastructure related changes."),
        Pattern(regex=case_insensetive("comment"), emoji=":bulb:", description="Add or update comments in source code."),
        Pattern(regex=case_insensetive("experiment"), emoji=":alembic:", description="Perform experiments."),
        # LOG
        Pattern(regex=contain_words("add", "log"), emoji=":loud_sound:", description="Add or update logs."),
        Pattern(regex=contain_words("update", "log"), emoji=":loud_sound:", description="Add or update logs."),
        Pattern(regex=contain_words("remove", "log"), emoji=":mute:", description="Remove logs."),
        # NotCommon
        Pattern(regex=case_insensetive("analytics"), emoji=":chart_with_upwards_trend:", description="Add or update analytics or track code."),
        Pattern(regex=case_insensetive("license"), emoji=":page_facing_up:", description="Add or update license."),
        Pattern(regex=case_insensetive("contributor"), emoji=":busts_in_silhouette:", description="Add or update contributor(s)."),
        Pattern(regex=case_insensetive("gitignore"), emoji=":see_no_evil:", description="Add or update a .gitignore file."),
        Pattern(regex="SEO", emoji=":mag:", description="Improve SEO."),
        Pattern(regex=case_insensetive("sponsorships"), emoji=":money_with_wings:", description="Add sponsorships or money related infrastructure."),
        Pattern(regex=case_insensetive("snapshot"), emoji=":camera_flash:", description="Add or update snapshots."),
        Pattern(regex=case_insensetive("healthcheck"), emoji=":stethoscope:", description="Add or update healthcheck."),
        Pattern(regex=case_insensetive("authorization"), emoji=":passport_control:", description="Work on code related to authorization, roles and permissions."),
        # IDK
        Pattern(regex=case_insensetive("accessibility"), emoji=":wheelchair:", description="Improve accessibility."),
        Pattern(regex=case_insensetive("drunk"), emoji=":beers:", description="Write code drunkenly."),
        Pattern(regex=case_insensetive("literal"), emoji=":speech_balloon:", description="Add or update text and literals."),
        Pattern(regex=case_insensetive("responsive"), emoji=":iphone:", description="Work on responsive design."),
        Pattern(regex=case_insensetive("user experience"), emoji=":children_crossing:", description="Improve user experience / usability."),
        Pattern(regex=case_insensetive("easter egg"), emoji=":egg:", description="Add or update an easter egg."),
        Pattern(regex=case_insensetive("seed"), emoji=":seedling:", description="Add or update seed files."),
        Pattern(regex=case_insensetive("animation"), emoji=":dizzy:", description="Add or update animations and transitions."),
        Pattern(regex=contain_words("compiler", "warning"), emoji=":rotating_light:", description="Fix compiler / linter warnings."),
        Pattern(regex=contain_words("bad", "code"), emoji=":poop:", description="Write bad code that needs to be improved."),
        Pattern(regex=contain_words("external","API","changes"), emoji=":alien:", description="Update code due to external API changes."),
        Pattern(regex=contain_words("add", "assets"), emoji=":bento:", description="Add or update assets."),
        Pattern(regex=contain_words("update", "assets"), emoji=":bento:", description="Add or update assets."),
        Pattern(regex=contain_words("add", "feature", "flag"), emoji=":triangular_flag_on_post:", description="Add, update, or remove feature flags."),
        Pattern(regex=contain_words("update", "feature", "flag"), emoji=":triangular_flag_on_post:", description="Add, update, or remove feature flags."),
        Pattern(regex=contain_words("data","exploration"), emoji=":monocle_face:", description="Data exploration/inspection."),
        Pattern(regex=contain_words("developer","experience"), emoji=":technologist:", description="Improve developer experience."),
        # FIX
        Pattern(regex=contain_words("Critical","fix"), emoji=":ambulance:", description="Critical hotfix."),
        Pattern(regex=contain_words("important","fix"), emoji=":ambulance:", description="Critical hotfix."),
        Pattern(regex=case_insensetive("bug"), emoji=":bug:", description="Fix a bug."),
        Pattern(regex=case_insensetive("fix"), emoji=":adhesive_bandage:", description="Simple fix for a non-critical issue."),
        Pattern(regex=contain_words("catch","error"), emoji=":goal_net:", description="Catch errors."),
        # REMOVE 
        Pattern(regex=case_insensetive("deprecate"), emoji=":wastebasket:", description="Deprecate code that needs to be cleaned up."),
        Pattern(regex=contain_words("remove","dead"), emoji=":coffin:", description="Remove dead code."),
        # Refactor
        Pattern(regex=case_insensetive("architectural"), emoji=":building_construction:", description="Make architectural changes."),
        Pattern(regex=case_insensetive("architecture"), emoji=":building_construction:", description="Make architectural changes."),
        Pattern(regex=case_insensetive("structure"), emoji=":art:", description="Improve structure / format of the code."),
        Pattern(regex=case_insensetive("Improve"), emoji=":zap:", description="Improve performance."),
        Pattern(regex=case_insensetive("Refactor"), emoji=":recycle:", description="Refactor code."),
        Pattern(regex=case_insensetive("Revert"), emoji=":rewind:", description="Revert changes."),
        # TEST
        Pattern(regex=contain_words("fail","test"), emoji=":test_tube:", description="Add a failing test."),
        Pattern(regex=case_insensetive("test"), emoji=":white_check_mark:", description="Add, update, or pass tests."),
        Pattern(regex=case_insensetive("Mock"), emoji=":clown_face:", description="Mock things."),
        # Security
        Pattern(regex=case_insensetive("security"), emoji=":lock:", description="Fix security issues."),
        Pattern(regex=case_insensetive("secret"), emoji=":closed_lock_with_key:", description="Add or update secrets."),
        # Feature
        Pattern(regex=case_insensetive("initial"), emoji=":tada:", description="Begin a project."),
        Pattern(regex=case_insensetive("begin"), emoji=":tada:", description="Begin a project."),
        Pattern(regex=case_insensetive("Add"), emoji=":sparkles:", description="Introduce new features."),
        Pattern(regex=case_insensetive("Update"), emoji=":hammer:", description="Add or update development scripts."),
        Pattern(regex=case_insensetive("Remove"), emoji=":fire:", description="Remove code or files."),
        Pattern(regex=case_insensetive("typo"), emoji=":pencil2:", description="Fix typos."),
        Pattern(regex=case_insensetive("documentation"), emoji=":memo:", description="Add or update documentation."),
        Pattern(regex=case_insensetive("document"), emoji=":memo:", description="Add or update documentation."),
        Pattern(regex=contain_words("breaking", "change"), emoji=":boom:", description="Introduce breaking changes."),
]

def get_msg(msg:str) -> str:
    for pattern in patterns:
        if re.search(pattern.regex, msg):
            return f"{pattern.emoji} {msg}"
    return msg

