from random import randint

class Map:
    def __init__(self, w, h):
        self.width = w * 2 + 1
        self.height = h * 2 + 1
        self.cnt = 0
        self.map = [[' '] * (2 * w + 1) for _ in range(2 * h + 1)]
        self.gold = [[0] * (2 * w + 1) for _ in range(2 * h + 1)]
        self.holes = {}
        self.players = [[[] for _ in range(2 * w + 1)] for _ in range(2 * h + 1)]

    def escape(self):
        p = randint(1, self.cnt)
        self.cnt -= 1
        if p == 1:
            return True
        else:
            return False


class Player:
    x: int
    y: int

    def __init__(self, player_id: int, x: int, y: int, lives=3, shot=3, grenade=3):
        self.id = player_id
        self.lives = lives
        self.shot = shot
        self.grenade = grenade
        self.x = x * 2
        self.y = y * 2

    def river(self, this_map: Map):
        if this_map.map[self.y][self.x] == '^':
            self.y -= 2
        elif this_map.map[self.y][self.x] == 'V':
            self.y += 2
        elif this_map.map[self.y][self.x] == '<':
            self.x -= 2
        elif this_map.map[self.y][self.x] == '>':
            self.x += 2

    def effects(self, bring: bool, this_map: Map):
        if this_map.map[self.y][self.x] == 'M':
            self.lives = 3
            return "The player {" + str(self.id) + "} is healed."
        elif this_map.map[self.y][self.x] == 'A':
            self.shot = 3
            self.grenade = 3
            return "The player {" + str(self.id) + "} has got new arsenal."
        elif this_map.map[self.y][self.x] == 'D':
            this_map.players[self.y][self.x].remove(self.id)
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            self.x, self.y = this_map.holes[(self.x, self.y)][0], this_map.holes[(self.x, self.y)][1]
            this_map.players[self.y][self.x].append(self.id)
            if bring:
                this_map.gold[self.y][self.x] += 1
            if this_map.gold[self.y][self.x] != 0:
                return "The hole with gold."
            else:
                return "The hole."
        elif this_map.map[self.y][self.x] == '0':
            if this_map.gold[self.y][self.x] != 0:
                return "The river mouth with gold."
            return "The river mouth."
        elif this_map.map[self.y][self.x] in ['^', 'V', '<', '>']:
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            this_map.players[self.y][self.x].remove(self.id)
            self.river(this_map)
            self.river(this_map)
            if bring:
                this_map.gold[self.y][self.x] += 1
            this_map.players[self.y][self.x].append(self.id)
            if this_map.map[self.y][self.x] == '0':
                if this_map.gold[self.y][self.x] != 0:
                    return "The river mouth with gold."
                return "The river mouth."
            else:
                if this_map.gold[self.y][self.x] != 0:
                    return "The river with gold."
                return "The river."
        else:
            if this_map.gold[self.y][self.x] != 0:
                return "Gold."
            return "Nothing."

    def move(self, direction: str, bring: bool, this_map: Map, players: dict[str, 'Player']):
        if self.lives == 0:
            bring = False
        if direction == "shoot up":
            if self.lives == 0:
                return "You can`t shoot because you`re dead."
            if self.shot == 0:
                return "You haven't got any bullet."
            self.shot -= 1
            sh_y: int = self.y - 1
            while sh_y > 0 and this_map.players[sh_y][self.x] != '-':
                if not this_map.players[sh_y][self.x]:
                    sh_y -= 1
                elif len(this_map.players[sh_y][self.x]) == 1:
                    return "Player {" + str(this_map.players[sh_y][self.x][0]) + "} is wounded."
                else:
                    s = "Players "
                    for P in this_map.players[sh_y][self.x]:
                        if players[P].lives != 0:
                            players[P].lives -= 1
                            s += "{" + str(P) + "}, "
                    s += "are wounded."
                    return s
            return "Nobody is wounded."
        elif direction == "shoot down":
            if self.lives == 0:
                return "You can`t shoot because you`re dead."
            if self.shot == 0:
                return "You haven't got any bullet."
            self.shot -= 1
            sh_y = self.y + 1
            while sh_y < this_map.height and this_map.players[sh_y][self.x] != '-':
                if not this_map.players[sh_y][self.x]:
                    sh_y += 1
                elif len(this_map.players[sh_y][self.x]) == 1:
                    return "Player {" + str(this_map.players[sh_y][self.x][0]) + "} is wounded."
                else:
                    s = "Players "
                    for P in this_map.players[sh_y][self.x]:
                        if players[P].lives != 0:
                            players[P].lives -= 1
                            s += "{" + str(P) + "}, "
                    s += "are wounded."
                    return s
            return "Nobody is wounded."
        elif direction == "shoot left":
            if self.lives == 0:
                return "You can`t shoot because you`re dead."
            if self.shot == 0:
                return "You haven't got any bullet."
            self.shot -= 1
            sh_x = self.x - 1
            while sh_x > 0 and this_map.players[self.y][sh_x] != '-':
                if not this_map.players[self.y][sh_x]:
                    sh_x -= 1
                elif len(this_map.players[self.y][sh_x]) == 1:
                    return "Player {" + str(this_map.players[self.y][sh_x][0]) + "} is wounded."
                else:
                    s = "Players "
                    for P in this_map.players[self.y][sh_x]:
                        if players[P].lives != 0:
                            players[P].lives -= 1
                            s += "{" + str(P) + "}, "
                    s += "are wounded."
                    return s
            return "Nobody is wounded."
        elif direction == "shoot right":
            if self.lives == 0:
                return "You can`t shoot because you`re dead."
            if self.shot == 0:
                return "You haven't got any bullet."
            self.shot -= 1
            sh_x = self.x + 1
            while sh_x < this_map.width and this_map.players[self.y][sh_x] != '-':
                if not this_map.players[self.y][sh_x]:
                    sh_x += 1
                elif len(this_map.players[self.y][sh_x]) == 1:
                    return "Player {" + str(this_map.players[self.y][sh_x][0]) + "} is wounded."
                else:
                    s = "Players "
                    for P in this_map.players[self.y][sh_x]:
                        if players[P].lives != 0:
                            players[P].lives -= 1
                            s += "{" + str(P) + "}, "
                    s += "are wounded."
                    return s
            return "Nobody is wounded."
        elif direction == "detonation":
            if self.lives == 0:
                return "You can`t throw a grenade because you`re dead."
            if self.grenade == 0:
                return "You haven't gon any grenade."
            self.grenade -= 1
            if self.x > 1:
                this_map.map[self.y][self.x - 1] = '+'
            if self.y > 1:
                this_map.map[self.y - 1][self.x] = '+'
            if self.x < this_map.width - 2:
                this_map.map[self.y][self.x + 1] = '+'
            if self.y < this_map.height - 2:
                this_map.map[self.y + 1][self.x] = '+'
            return "OK"
        elif direction == "jump":
            return self.effects(bring, this_map)
        elif direction == "up":
            if this_map.map[self.y - 1][self.x] == '-':
                return "You hit a wall."
            elif self.y - 1 == 0:
                if self.lives == 0:
                    return "You can`t get out of the maze because you`re dead."
                if bring and this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                    if this_map.escape():
                        return "Win!"
                    else:
                        return "Your gold is fake."
                else:
                    return "You can`t get out of the maze without a gold."
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            this_map.players[self.y][self.x].remove(self.id)
            self.y -= 2
            if bring:
                this_map.gold[self.y][self.x] += 1
            this_map.players[self.y][self.x].append(self.id)
            if this_map.map[self.y][self.x] == 'V' or this_map.map[self.y + 2][self.x] == '^':
                if this_map.map[self.y][self.x] == '0':
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river mouth with gold."
                    return "The river mouth."
                else:
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river with gold."
                    return "The river."
            else:
                return self.effects(bring, this_map)
        elif direction == "down":
            if this_map.map[self.y + 1][self.x] == '-':
                return "You hit a wall."
            elif self.y + 1 == this_map.height - 1:
                if self.lives == 0:
                    return "You can`t get out of the maze because you`re dead."
                if bring and this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                    if this_map.escape():
                        return "Win!"
                    else:
                        return "Your gold is fake."
                else:
                    return "You can`t get out of the maze without a gold."
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            this_map.players[self.y][self.x].remove(self.id)
            self.y += 2
            if bring:
                this_map.gold[self.y][self.x] += 1
            this_map.players[self.y][self.x].append(self.id)
            if this_map.map[self.y][self.x] == '^' or this_map.map[self.y - 2][self.x] == 'V':
                if this_map.map[self.y][self.x] == '0':
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river mouth with gold."
                    return "The river mouth."
                else:
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river with gold."
                    return "The river."
            else:
                return self.effects(bring, this_map)
        elif direction == "left":
            if this_map.map[self.y][self.x - 1] == '-':
                return "You hit a wall."
            elif self.x - 1 == 0:
                if self.lives == 0:
                    return "You can`t get out of the maze because you`re dead."
                if bring and this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                    if this_map.escape():
                        return "Win!"
                    else:
                        return "Your gold is fake."
                else:
                    return "You can`t get out of the maze without a gold."
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            this_map.players[self.y][self.x].remove(self.id)
            self.x -= 2
            if bring:
                this_map.gold[self.y][self.x] += 1
            this_map.players[self.y][self.x].append(self.id)
            if this_map.map[self.y][self.x] == '>' or this_map.map[self.y][self.x + 2] == '<':
                if this_map.map[self.y][self.x] == '0':
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river mouth with gold."
                    return "The river mouth."
                else:
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river with gold."
                    return "The river."
            else:
                return self.effects(bring, this_map)
        elif direction == "right":
            if this_map.map[self.y][self.x + 1] == '-':
                return "You hit a wall."
            elif self.x + 1 == this_map.width - 1:
                if self.lives == 0:
                    return "You can`t get out of the maze because you`re dead."
                if bring and this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                    if this_map.escape():
                        return "Win!"
                    else:
                        return "Your gold is fake."
                else:
                    return "You can`t get out of the maze without a gold."
            if bring:
                if this_map.gold[self.y][self.x] != 0:
                    this_map.gold[self.y][self.x] -= 1
                else:
                    bring = False
            this_map.players[self.y][self.x].remove(self.id)
            self.x += 2
            if bring:
                this_map.gold[self.y][self.x] += 1
            this_map.players[self.y][self.x].append(self.id)
            if this_map.map[self.y][self.x] == '<' or this_map.map[self.y][self.x - 2] == '>':
                if this_map.map[self.y][self.x] == '0':
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river mouth with gold."
                    return "The river mouth."
                else:
                    if this_map.gold[self.y][self.x] != 0:
                        return "The river with gold."
                    return "The river."
            else:
                return self.effects(bring, this_map)


class Session:
    players = {}
    new_map: Map

    def __init__(self):
        s = "5 5\n+-+-+-+++-+\n-M-0+<- -0-\n+++++-+++++\n-D+ + + -A-\n+-+++++++++\n-0-D+T-T+ -\n+++-+++++-+\n-^- + - -D-\n+++++-+++++\n-^+ + + +D-\n+-+-+-+-+-+\nD(0; 1)>>D(4; 4)\nD(4; 4)>>D(4; 3)\nD(4; 3)>>D(0; 1)\nD(1; 2)>>D(1; 2)"
        inp = s.split("\n")
        w, h = map(int, inp[0].split())
        self.new_map = Map(w, h)
        for i in range(h * 2 + 1):
            for j in range(w * 2 + 1):
                self.new_map.map[i][j] = inp[i + 1][j]
                if self.new_map.map[i][j] == 'T' or self.new_map.map[i][j] == 'F':
                    self.new_map.cnt += 1
                    self.new_map.gold[i][j] = 1
                    self.new_map.map[i][j] = ' '
        for i in range(h * 2 + 2, len(inp)):
            a, b, c = inp[i].split('(')
            d, e = b.split(')')
            x1, y1 = map(int, d.split("; "))
            f, g = c.split(')')
            x2, y2 = map(int, f.split("; "))
            self.new_map.holes[(x1 * 2, y1 * 2)] = (x2 * 2, y2 * 2)

    def add_new_player(self, player_id: int, x: int, y: int):
        self.players[player_id] = Player(player_id, x, y)
        self.new_map.players[y * 2][x * 2].append(player_id)
