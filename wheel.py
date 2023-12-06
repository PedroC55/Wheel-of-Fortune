############# import #############

from __future__ import annotations
import random
import os


############# Wheel #############

class Wheel:
    def __init__(self: Wheel):
        self.wheel = [5000, "Bancarrota", 750, 1000, 600, 250, "Vogal Grátis", 1500, 450, 200, "Ficha de recuperação", 150, 800, 900, 50, 850, 1200, 2000, "Perde Vez", 100]
        
        pass
    
    def spin(self: Wheel) -> int:
        return self.wheel[random.randint(0, len(self.wheel)-1)]
        
 

############# Puzzle #############

class Puzzle:
    def __init__(self: Puzzle, secret_txt: str, theme: str):
        self.word = secret_txt
        self.in_secret_word = self.secret(secret_txt)
        self.theme = theme
        self.wheel_active = 1
        self.buy_vowels_active = 1
    
    def secret(self, text):
        secret_chars = {char: '-' for char in 'abcdefghijklmnopqrstuvwxyz'}
        return ''.join(secret_chars.get(char.lower(), char) for char in text)
    

    def is_finished(self):
        if self.in_secret_word == self.word:
            return True
        else:
            return False

    def is_vowel(self, char):
        if char.lower() in 'aeiou':
            return  True
        else:
            return False

    def show_puzzle(self: Puzzle):
        print(f'>> {self.theme}: {self.in_secret_word}')

    def check_answer(self, answer):
        if answer.lower() == self.word.lower():
            self.in_secret_word = answer.upper()
            return True
        else:
            return False
            
    def all_consonants_revealed(self):
        revealed_consonants = list(c.lower() for c in self.in_secret_word if c.isalpha() and c.lower() not in 'aeiou')
        secret_consonants = list(c.lower() for c in self.word if c.isalpha() and c.lower() not in 'aeiou')
        if revealed_consonants == secret_consonants:
            self.wheel_active = 0
            print("Todas as consoantes estão à vista! A roleta está desativada.")
    
    def all_vowels_revealed(self):
        revealed_consonants = list(c.lower() for c in self.in_secret_word if c.isalpha() and c.lower() in 'aeiou')
        secret_consonants = list(c.lower() for c in self.word if c.isalpha() and c.lower() in 'aeiou')
        if revealed_consonants == secret_consonants:
            self.buy_vowels_active = 0
            print("Todas as vogais estão à vista! A compra de vogais está desativada.")

    def reveal_consonant(self, consonant, players, current_player,result):
        count = 0
        number_interactions = 0
        revealed_word = ''
        
        if self.is_vowel(consonant) == True:
            print("A letra inserida não é uma consoante!")
            return False
        
        for char in self.in_secret_word:
            if char.lower() == consonant:
                print("Essa já saiu e está à vista.")
                return False

        for char in self.word:
            if char.lower() == consonant:
                count += 1
                if char.isupper():
                    revealed_word += consonant.upper()
                else:
                    revealed_word += consonant.lower()
            else:
                revealed_word += self.in_secret_word[number_interactions]
            number_interactions += 1
        
        self.in_secret_word = revealed_word
        if count > 0:
            current_player.update_money(count*result)
        print(f'Encontradas {count} ocorrências de {consonant} valendo {count}*{result}={count*result}. {players.print_players()}')
        if count == 0:
            return False
        return True

    def reveal_vowel(self, vowel, players):
        count = 0
        number_interactions = 0
        revealed_word = ''
        if self.is_vowel(vowel) == False:
            print("A letra inserida não é uma vogal!")
            return False
        
        for char in self.in_secret_word:
            if char.lower() == vowel:
                print("Essa já saiu e está à vista.")
                return False

        for char in self.word:
            if char.lower() == vowel:
                count += 1
                if char.isupper():
                    revealed_word += vowel.upper()
                else:
                    revealed_word += vowel.lower()
            else:
                revealed_word += self.in_secret_word[number_interactions]
            number_interactions += 1
        
        self.in_secret_word = revealed_word
        print(f'Encontradas {count} ocorrências de {vowel}. {players.print_players()}')
        if count == 0:
            players.nextplayer()
        return True


############# Puzzles #############

class Puzzles:
    def __init__(self: Puzzles, file_name: str):
        self.puzzles = []           # todos os puzzles
        self.load(file_name)

    def load(self: Puzzles, file_name: str):
        with open(file_name, 'r') as file:
            for line in file:
                self.puzzles.append(line.strip())
        pass   
    def erase_puzzle(self, puzzle):
        puzzle = puzzle.theme + ": " + puzzle.word
        self.puzzles.pop(self.puzzles.index(puzzle))


############# Player #############

class Player:
    def __init__(self: Player, name: str):
        self.name = name
        self.money = 0
        self.fichas = 0
        self.money_won_round = 0
        
    def get_tokens(self):
        return self.fichas
    
    def spend_token(self):
        self.fichas -= 1

    def end_round(self, winner):
        if winner.name == self.name:
            self.money += self.money_won_round
            self.loose_all_money()
        else:
            self.loose_all_money()

    def get_current_income(self):
        return self.money
    
    def get_current_round_income(self):
        return self.money_won_round
    
    def update_money(self, value):
        self.money_won_round += value
    
    def bought_vowel(self):
        self.money_won_round = self.money_won_round - 250
    
    def loose_all_money(self):
        self.money_won_round = 0

    def win_token(self):
        self.fichas += 1
    
    def winner(self):
        self.money = self.money + 6000


############# Players #############

class Players:
    def __init__(self: Players, names: list[str]):
        self.all = []
        self.current = 0
        for name in names:
            self.all.append(Player(name))
    
    def nextplayer(self):
        if self.current < len(self.all) - 1:
            self.current += 1
        else:
            self.current = 0

    def get_current_player(self: Players) -> Player:
        current_player = self.all[self.current]
        return current_player

    def print_players(self):
        str_final = ""
        for i, player in enumerate(self.all):
            if i == len(self.all) - 1:
                str_final += f'{player.name}' + " = " + f'{player.get_current_round_income()} euros.' 
            else:
                str_final += f'{player.name}' + " = " + f'{player.get_current_round_income()} euros, ' 
            
        return str_final
    
    
    

    def check_winner_game(self):
        cuurent_winner = []
        for player in self.all:
            if cuurent_winner == []:
                cuurent_winner.append(player)
            else:
                if player.get_current_income() >= cuurent_winner[0].get_current_income():
                    cuurent_winner.append(player)
        
        for player in cuurent_winner:
            player.money = player.money + int(6000 / len(cuurent_winner))
        return cuurent_winner
    

############# Game #############

class Game:
    def __init__(self: Game, file_name: str, names: list[str], rounds: int):
        self.players = Players(names)
        self.running = True
        self.all_puzzles = Puzzles(file_name)
        self.wheel = Wheel()
        self.rounds = rounds
        
    
    def create_puzzle(self):
        rand = random.randint(0, len(self.all_puzzles.puzzles)-1)
        cr_puzzle = self.all_puzzles.puzzles[rand]
        cr_puzzle = cr_puzzle.split(":")
        secret = cr_puzzle[1].lstrip()
        theme = cr_puzzle[0]
        self.current_puzzle = Puzzle(secret, theme)
        return self.current_puzzle
    
    def finish_round(self, winner, puzzle):
        for player in self.players.all:
            player.end_round(winner)
        self.all_puzzles.erase_puzzle(puzzle)
        self.running = False
    
    def start_new_round(self):
        self.running = True
        
    def get_current_player(self: Game) -> Player:
        return self.players.get_current_player()
    
    def get_inventory(self):
        count = 1
        print(f'Inventário:')
        print(f'N. Nome\t\tFichas\tRondas\tJogos')
        for player in self.players.all:     
            print(f'{count} {player.name:<13}\t{player.get_tokens()}\t{player.get_current_round_income()}\t{player.get_current_income()}')
            count += 1
        
    
    # O mÃ©todo spy escreve informaÃ§Ã£o tÃ©cnica.
    # NÃ£o Ã© considerado um mÃ©todo de interaÃ§Ã£o com o utilizador.
    # Ã‰ mais prÃ¡tico definir o mÃ©todo aqui do que na classe UI.
    def spy(self: Game, current_round, current_puzzle, p, game_finished):
        if game_finished:
            print(f'# {current_round} 0 0')
        else:
            print(f'# {current_round} {current_puzzle.wheel_active} {current_puzzle.buy_vowels_active}')
        print(f'# {current_puzzle.theme}: {current_puzzle.word}')
        print(f'# {current_puzzle.theme}: {current_puzzle.in_secret_word}')
        for player in self.players.all:
            if player.name == p.name:
                print(f'# * {player.fichas} {player.money_won_round:05d} {player.money:05d} {player.name}')
            else:
                print(f'# - {player.fichas} {player.money_won_round:05d} {player.money:05d} {player.name}')


############# Mooshak #############

# NÃ£o altere esta funÃ§Ã£o!

def mooshak():
    FILE_NAME = "puzzles.txt"
    m = os.environ.get('MOOSHAK')
    if m:
        eval(m)
        return os.environ.get('MOOSHAK_PUZZLES')
    else:
        return FILE_NAME


############# UI #############

class UI:   # User Interface
    def __init__(self: UI, players, rounds):
        file_name = "./" + mooshak()              # linha necessÃ¡ria
        if len(players) < 1 or len(players) > 4:
            self.error("Número de jogadores tem de estar entre 1 e 4")
        else:
            self.players = players
        
        if rounds < 1 or rounds > 4:
            self.error("Número de rodadas tem de estar entre 1 e 4")
        else:
            self.rounds = rounds
        if os.path.isfile(file_name):
            self.game = Game(file_name, players, rounds)
        else:
            self.error("Ficheiro puzzles.txt não existe")
   
    def error(self: UI, mesg: str):
        raise Exception(f"{mesg}!")
    

    def end_round(self, p, current_round):
        self.game.finish_round(p, self.puzzle)
        print(f'O concorrente "{p.name}" venceu a ronda número {current_round}.')
        print(f'Inventário no final da ronda número {current_round}:')
        self.game.get_inventory()
        
        

    def end_game(self):
        winner = self.game.players.check_winner_game()
        print(f'Final do jogo! Este jogo teve {self.rounds} ronda(s).')
        for player in winner:
            print(f'O concorrente "{player.name}" venceu o jogo e leva para casa {player.get_current_income()} euros.')
        for player in self.game.players.all:
            
            if player not in winner:
                print(f'O concorrente "{player.name}" leva para casa {player.get_current_income()} euros.')
        



    def loose_turn(self,p):
        if p.get_tokens() > 0:
            spend_token = input("Você vai perder a vez. Deseja usar agora uma ficha de recuperação (s/n). ")
            if spend_token == 's':
                p.spend_token()
                print("Afinal não perde a vez.")
            else:
                print("Perde a vez. Para a próxima esteja com mais atenção.")
                self.game.players.nextplayer()
        else:
            print("Perde a vez. Para a próxima esteja com mais atenção.")
            self.game.players.nextplayer()
    def buy_vowel(self,p, current_round):
        vowel = input("Qual a vogal? ")
        bool = self.puzzle.reveal_vowel(vowel, self.game.players)
        if bool == False:
            self.loose_turn(p)
        else:
            if self.puzzle.is_finished():
                self.end_round(p, current_round)
            else:    
                self.puzzle.show_puzzle()
    
    def spin_wheel(self, p, current_round):
        result = self.game.wheel.spin()
        print(result)
        if result != "Bancarrota" and result != "Perde Vez" and result != "Vogal Grátis" and result != "Ficha de recuperação":
            cons = input("Qual a consoante? ")
            
            
            bool = self.puzzle.reveal_consonant(cons,self.game.players,p, result)
            if bool == False:
                self.loose_turn(p)
            else:
                if self.puzzle.is_finished():
                    self.end_round(p, current_round)
                else:    
                    self.puzzle.show_puzzle()
        elif result == "Vogal Grátis":
            self.buy_vowel(p, current_round)
        
        elif result == "Bancarrota":
            p.loose_all_money()
            print(f'Perde todo o dinheiro obtido nesta ronda e também perde a vez.')
            self.game.players.nextplayer()
            

        elif result == "Ficha de recuperação":
            p.win_token()
            print(f'O seu total de fichas de recuperação é {p.get_tokens()}.')
        
        elif result == "Perde Vez":
            self.game.players.nextplayer()

    def finish_puzzle(self,p, current_round):
        answer = input(f'Resolva o puzzle! >> {self.puzzle.theme}: ')
        bool = self.puzzle.check_answer(answer)
        if bool == False:
            print("Errado!")
            self.loose_turn(p)
        else:
            print("Certo!")
            self.puzzle.show_puzzle()
            self.end_round(p, current_round)

    
    def input_command(self: UI) -> str:
        p = self.game.get_current_player()
        command_line = input(f"[{p.name}]: ")
        command = command_line.strip().upper()
        return command, p
    
    def print_commands(self: UI):
        print("Commands: \n c - Comandos (listar comandos) \n i - Inventário (mostrar) \n f - Finalizar puzzle \n p - Puzzle (mostrar) \n r - Roleta (rodar) \n v - Vogal (comprar) \n # - Espiar (mooshak) \n q - Quit (terminar imediatamente)")

    def show_all_puzzles(self):
        print(self.game.all_puzzles.puzzles)


    def command_spy(self: UI, current_round, current_puzzle, p, game_finished):
        self.game.spy(current_round, current_puzzle, p, game_finished)        # linha necessÃ¡ria
    
    def command_authors(self: UI):
        print("Autores:")
        print("   Nº67837 Inês Marques")
        print("   Nº68505 Margarida Fonseca")
    
    def command_quit(self: UI):
        raise SystemExit
        
    
    def command_help(self: UI):
        print("Comandos disponíveis: #/C/R/P/F/I/V/A/Q")
        pass
    
    def interpreter(self: UI, current_round):
        # inspire-se no interpretador do final da teÃ³rica 18
        while self.game.running:
            command, p = self.input_command()
            if command == ' ': pass
            if command == '#': self.command_spy(current_round, self.puzzle, p, False)
            if command == 'C': self.print_commands()
            if command == 'R':
                if self.puzzle.wheel_active == 1:
                    self.spin_wheel(p, current_round)
                    self.puzzle.all_consonants_revealed()
                else:
                    print("Todas as consoantes estão à vista! A roleta está desativada.")
                if self.puzzle.wheel_active == 0 and self.puzzle.buy_vowels_active == 0:
                    self.end_round(p,current_round)
                
            if command == 'P': self.puzzle.show_puzzle()
            if command == 'F': self.finish_puzzle(p, current_round)
            if command == 'I': self.game.get_inventory()
            if command == 'V':
                if self.puzzle.buy_vowels_active == 1:
                    if p.get_current_round_income() >= 250:
                        p.bought_vowel()
                        self.buy_vowel(p,current_round)
                    else:
                        print("Você não tem dinheiro suficiente para comprar uma vogal.")
                        self.loose_turn(p)
                    self.puzzle.all_vowels_revealed()
                else:
                    print("Todas as vogais estão à vista! A compra de vogais está desativada.")
                
                if self.puzzle.wheel_active == 0 and self.puzzle.buy_vowels_active == 0:
                    self.end_round(p,current_round)
                
            if command == 'A': self.command_authors()
            if command == 'Q': 
                self.command_spy(current_round, self.puzzle, p, False)
                self.command_quit()
            if command != ' ' and  command != '#' and  command != 'C' and  command != 'R' and  command != 'P' and  command != 'F' and  command != 'I' and  command != 'V' and  command != 'A' and  command != 'Q' : 
                
                self.command_help()
            else: pass
        return p

    
    def run(self: UI):
        count_rounds = 1
        for i in range(self.rounds):
            print(f'Vamos começar a ronda {count_rounds}. Eis o puzzle. Boa sorte!')
            self.game.start_new_round()
            self.puzzle = self.game.create_puzzle()
            self.puzzle.show_puzzle()
            p = self.interpreter(count_rounds)
            if self.rounds == count_rounds:
                self.end_game()
                self.command_spy(count_rounds, self.puzzle, p, True)        # linha necessÃ¡ria
                print("Adeus!")
            else:
                count_rounds += 1


############# main #############

def main():
    print(f'Bem-vindo/a ao jogo "A Roda da Sorte"!')
    rondas = input(f'Quantas rondas? ')
    while not rondas.isdigit():
        print("Por favor, insira um número.")
        rondas = input(f'Quantas rondas? ')
    rondas = int(rondas)
    players = []
    
    nConcorrentes = input(f'Quantos concorrentes? ')
    while not nConcorrentes.isdigit():
        print("Por favor, insira um número.")
        nConcorrentes = input(f'Quantos concorrentes? ')
    nConcorrentes = int(nConcorrentes)
    for i in range(nConcorrentes):
        player = input(f'Nome do concorrente número {i+1}?  ')
        players.append(player)
    
    ui = UI(players, rondas)
    ui.run()

main()