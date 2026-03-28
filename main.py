import init_django_orm  # noqa: F401
import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as file:
        players_data = json.load(file)

    for nickname, data in players_data.items():

        race_data = data.get("race")
        if not race_data:
            continue

        race, _ = Race.objects.get_or_create(
            name=race_data.get("name"),
            defaults={"description": race_data.get("description", "")}
        )

        skills_list = race_data.get("skills", [])
        for skill_info in skills_list:
            Skill.objects.get_or_create(
                name=skill_info.get("name"),
                defaults={
                    "race": race,
                    "bonus": skill_info.get("bonus", "")
                }
            )

        guild_data = data.get("guild")
        guild = None
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data.get("name"),
                defaults={"description": guild_data.get("description")}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": data.get("email"),
                "bio": data.get("bio", ""),
                "race": race,
                "guild": guild,
            }
        )


if __name__ == "__main__":
    main()