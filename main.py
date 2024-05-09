# This file is for strategy

# TEACHER version

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        # comment out one or the other
        self.runTutorial()
        # self.runShimshock()

    # version of run() that we write during the tutorial
    def runTutorial(self):
        # speed = 500
        # set_intent tells the bot what it's trying to do
        # self.set_intent(drive(speed))
        # self.set_intent(jumper())

        # print(f"my x position is: {self.me.location.x}")
        #self.set_intent(atba())

        # if already have an intent, let it finish
        if self.get_intent() is not None:
            return

        # do kickoff logic if haven't completed kickoff yet
        if self.kickoff_flag:
            print("kicking off") 
            self.set_intent(kickoff())
            return

        # desired usage
        if self.is_in_front_of_ball():
            print("offsides, retreating to own goal")
            self.set_intent(goto(self.friend_goal.location))

        if self.me.boost > 99:
            print("boost full, going for a short shot")
            self.set_intent(short_shot(self.foe_goal.location))
            return
        
        target_boost = self.get_closest_large_boost()
        if target_boost is not None:
            print("going for boost at", target_boost.location)
            self.set_intent(goto(target_boost.location))
            return

        print("I'm lost without an intent!")

        # # go to first boost in list
        # if len(available_boosts) > 0:
        #     self.set_intent(goto(available_boosts[0].location))
        #     print("going for boost index", available_boosts[0].index)
        # else:
        #     print("I'm lost without an intent")



        # # Shots
        # targets = {
        #     'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
        #     'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post) # reversed order to *exclude* own goal
        # }
        # hits = find_hits(self,targets)

        # # if int(self.time % 2) == 0:
        # #     print(hits)

        # if len(hits['at_opponent_goal']) > 0: # have a shot, take the first one
        #     self.set_intent(hits['at_opponent_goal'][0])
        #     print("try shot at opp goal")
        #     return
        # if len(hits['away_from_our_net']) > 0: # have a shot, take the first one
        #     self.set_intent(hits['away_from_our_net'][0])
        #     print("try clear ball")
        #     return
        

        # self.set_intent(atba()) # note: atba() doesn't clear the intent (need to override intent if want to change)
        # self.set_intent(short_shot(self.foe_goal.location))

    def closestBoostFromList(self, boostList):
        pass

        
    # version of run that I've tried experimenting with
    def runShimshock(self):
        speed = 500
        # set_intent tells the bot what it's trying to do
        # self.set_intent(drive(speed))
        # self.set_intent(jumper())

        # print(f"my x position is: {self.me.location.x}")
        #self.set_intent(atba())

        # do kickoff logic if haven't completed kickoff yet
        if self.kickoff_flag: 
            self.set_intent(kickoff())

        # otherwise regular game logic
        else:

            # shimshock custom logic: want to retreat if past the ball, otherwise aim for ball
            dist_ball_friend_goal = (self.ball.location - self.friend_goal.location).magnitude()
            dist_self_friend_goal = (self.me.location - self.friend_goal.location).magnitude()
            offsides = dist_self_friend_goal > dist_ball_friend_goal

            #print(f"ballDist={dist_ball_friend_goal}\tselfDist={dist_self_friend_goal}\toffsides={offsides}")
            if offsides:
                if self.team == 0:
                    print(f"Team {self.team}: offsides! back towards own goal")
                self.set_intent(goto(self.friend_goal.location))
            else:
                if self.team == 0:
                    print(f"Team {self.team}: go to ball!")
                ## basic aim at ball
                #self.set_intent(atba())

                ## shimshock improved? try to go to ball, but be pointing at foe goal when get to ball
                ball_to_foe_goal = (self.foe_goal.location - self.ball.location).normalize()
                self.set_intent(goto(self.ball.location, ball_to_foe_goal))

        
