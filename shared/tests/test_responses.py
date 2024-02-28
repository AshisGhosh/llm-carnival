dummy_game_state = {
  "success": True,
  "state": {
    "summary": "## Salient points of the conversation about the game:\n\n* **Combat Readiness:** \n    * The conversation establishes different states of combat readiness based on the situation and the player's perception of danger.\n    * The player's initial reaction to hearing a rustle in the bushes is to be in a state of high alert with their weapon drawn and senses heightened.\n    * When facing an enemy with a sword and pistols, the player's next action depends on the context of the battle and the available options.\n    * The player's options in a boss battle with a magic crystal include blocking and waiting for an opportunity, using the shield to deflect the enemy's next attack, or attacking with the sword.\n* **Combat Status:**\n    * The conversation discusses the current state of the combat, offering options to describe the situation in different ways.\n    * The player's current advantage in the fight is emphasized, allowing them to gain the upper hand or maintain their ground.\n* **Other topics:**\n    * The conversation includes questions about flying like a bird or teleporting, as well as inquiries about the meaning of the word \"entrepreneur\" and the history of the internet.",
    "context": [
      [
        "**Question:**\n\nWhat is the state of your combat readiness when you hear a rustling in the bushes behind you as you explore an ancient ruin, and what further information would you like me to provide to help determine your next action?\n\n**Possible Answer Responses:**\n\n* **High alert:** I would be in a state of high alert, with my weapon drawn and my senses on high. I would be vigilant and prepared for any potential threat. I would also assess the surrounding environment for any potential hiding spots or escape routes.\n* **Cautious caution:** I would be in a state of cautious caution, with my hand hovering near my weapon and my eyes wide open. I would be wary of my surroundings and listen intently for any further sounds or signs of danger.\n* **Full readiness:** I would be in a state of full readiness, with my weapon drawn, my senses heightened, and my mind focused on the source of the sound. I would be prepared for a fight and would be ready to act quickly if necessary.",
        "yes"
      ],
      [
        "**Question:**\n\nYou are in a heated battle, facing an enemy with two pistols and a sword. You have a pistol, a sword, and a shield. The enemy has already fired two shots at you, but you are still alive. What is your next action?\n\n**Possible Answer Responses:**\n\na) Block the sword and attempt to counter-attack\nb) Dodge the remaining bullets and draw your sword\nc) Shoot at the enemy with your pistol\nd) Use your shield to deflect the bullets",
        "yes"
      ],
      [
        "**Question:**\n\nYou are in a heated combat encounter with a boss enemy. You have a sword and shield, and the enemy has a sword and a magic crystal. Currently, the enemy has you pinned against a wall. You have the initiative, but the enemy is blocking your attacks. What is your next move?\n\n**Possible Answer Responses:**\n\na) Attack with the sword\nb) Block and wait for an opportunity\nc) Use the shield to deflect the enemy's next attack\nd) Cast a spell on the enemy",
        "yes"
      ],
      [
        "**Question:**\n\nIf you are in a combat scenario, what is the current state of the combat?\n\n**Answer Options:**\n\na) Stalemate\nb) You are winning\nc) You are losing\nd) You are parrying",
        "winning"
      ],
      [
        "**Question:**\n\nYou are in a combat scenario. What is the current state of the combat?\n\n**Possible Answers:**\n\na) The enemy is dominating you.\nb) You are holding your ground.\nc) You have gained the upper hand.\nd) The combat is even.",
        "yes"
      ],
      [
        "**Question:**\n\nWould you rather be able to fly like a bird or have the ability to teleport?\n\n**Possible Answer Responses:**\n\na) Fly like a bird\nb) Have the ability to teleport",
        "yes"
      ],
      [
        "## Question:\n\nWhat is your next question?\n\n**Possible answer responses:**\n\n* A multiple-choice question\n* A yes/no question",
        "no"
      ],
      [
        "**Question:**\n\nWhat is the meaning of the word \"entrepreneur\"?\n\n**Possible answers:**\n\na) A person who owns a business\nb) A person who is skilled at business\nc) A person who is willing to take risks\nd) A person who is good at managing money",
        "author"
      ],
      [
        "**Sure, here is the question:**\n\nWhat is the meaning of the word \"entrepreneur\"?\n\n**Possible answer responses:**\n\na) Someone who is good at starting businesses\nb) Someone who is good at marketing\nc) Someone who is good at managing finances\nd) Someone who is good at making products",
        "unknown"
      ],
      [
        "**Question:**\n\nWould you like to learn more about the history of the internet?\n\n**Possible Answer Responses:**\n\n- Yes, I would like to learn more about the history of the internet.\n- No, I am not interested in the history of the internet.\n- I would like to learn more about the evolution of the internet and its impact on society.",
        "yes"
      ]
    ]
  },
  "state_timestamp": "2024-02-28T00:19:09.341501",
  "timestamp": "2024-02-28T00:20:09.203305"
}

def get_dummy_game_state_response():
    return dummy_game_state