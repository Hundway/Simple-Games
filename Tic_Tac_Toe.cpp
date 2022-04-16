#include <iostream>
#include <cstring>

class Table{
private:
    char table[9];

public:
    Table(){
        for(int i = 0; i < 9; i++)
            table[i] = i + 49;
    }

    int setX(const int& pos){
        if(pos < 0 || pos > 8)
            return 0;
        if(table[pos] == 'X' || table[pos] == 'O')
            return 0;
        table[pos] = 'X';
        return 1;
    }

    int setO(const int& pos){
        if(pos < 0 || pos > 8)
            return 0;
        if(table[pos] == 'X' || table[pos] == 'O')
            return 0;
        table[pos] = 'O';
        return 1;
    }

    int checkWin(){
        int score = 0;
        // Checking lines
        for(int i = 0; i < 3; i++){
            score = 0;
            for(int j = 0; j < 3; j++){
                if(table[j + i * 3] == 'X')
                    score += 1;
                else if(table[j + i * 3] == 'O')
                    score -= 1;
            }
            if(score == 3)
                return 1;
            else if(score == -3)
                return 2;
        }
        // Checking columns
        for(int i = 0; i < 3; i++){
            score = 0;
            for(int j = 0; j < 3; j++){
                if(table[i + j * 3] == 'X')
                    score += 1;
                else if(table[i + j * 3] == 'O')
                    score -= 1;
            }
            if(score == 3)
                return 1;
            else if(score == -3)
                return 2;
        }
        // Checking diagonals
        if(table[0] == 'X' && table[4] == 'X' && table[8] == 'X')
            return 1;
        else if(table[0] == 'O' && table[4] == 'O' && table[8] == 'O')
            return 2;

        if(table[2] == 'X' && table[4] == 'X' && table[6] == 'X')
            return 1;
        else if(table[2] == 'O' && table[4] == 'O' && table[6] == 'O')
            return 2;

        return 0;
    }

    void printTable(){
        std::cout << "_" << table[0] << "_|_" << table[1] << "_|_"<< table[2] << "_" << std::endl;
        std::cout << "_" << table[3] << "_|_" << table[4] << "_|_"<< table[5] << "_" << std::endl;
        std::cout << " " << table[6] << " | " << table[7] << " | "<< table[8] << " " << std::endl;
    }
};

int main(){
    Table gameTable;
    int round = 0;
    int move, player_to_move;

    while(!gameTable.checkWin()){
        player_to_move = (round % 2) + 1;
        
        if(player_to_move == 1)
            do{
                gameTable.printTable();
                std::cout << "\nPlayer " << player_to_move << std::endl;
                std::cout << "Make your move : ";
                std::cin >> move;
                system("cls");
            }while(!gameTable.setX(--move));

        else if(player_to_move == 2)
            do{
                gameTable.printTable();
                std::cout << "\nPlayer " << player_to_move << std::endl;
                std::cout << "Make your move : ";
                std::cin >> move;
                system("cls");
            }while(!gameTable.setO(--move));

        round++;
    }

    gameTable.printTable();

    if(gameTable.checkWin() == 0)
        std::cout << "Draw !!!" << std::endl;
    else
        std::cout << "\nPlayer " << gameTable.checkWin() << " wins !!!" << std::endl;
    
    system("pause -> NULL");

    return 0;
}