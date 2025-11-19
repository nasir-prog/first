#include <iostream>
#include <string>
#include <vector>


//класс для персонажа огонь:
class Player{
private:
    int x,y;
    bool is_alive;
    unsigned int count_of_diamonds;
    unsigned int diamonds_on_the_level;
    std::string type_of_player;

public:
    Player(int start_x,int start_y,unsigned int diamonds_on_this_level,std::string type){
        x = start_x;
        y = start_y;
        count_of_diamonds = 0;
        diamonds_on_the_level = diamonds_on_this_level;
        is_alive = true;
        type_of_player = type;
    }
    
    ~Player(){
        //delete dx;
        //delete dy;
        //delete[] diamonds_array;
    }

    void move (int dx,int dy)
    {
        x = x + dx;
        y = y + dy;
    }

    void is_daimond_collected (int size_of_diamonds_array,int* diamonds_array){
        //сделать класс состоящий из кординат игрик и икс ,а diamonds_array -будет массивом таких объектов будет хранить координаты алмазов и потом проверять равна ли координата персонажа координате алмаза
    }

    bool is_finish_level(int x_door,int y_door)
    {
        if ((x == x_door)&& (y == y_door) && (count_of_diamonds == diamonds_on_the_level))
        {
            return true;
        }
        else{return false;}
    }

    bool is_died (int size_of_die_area_array,int* die_area_array)
    {
        //сделать класс состоящий из кординат игрик и икс ,а die_area_array -будет массивом таких объектов будет хранить координаты воды 
    }

    //Getters:
    int getX()
    {
        return x;
    }

    int getY()
    {
        return y;
    }

    bool getIsAlive()
    {
        return is_alive;
    }

    unsigned int getCountOfDiamonds()
    {
        return count_of_diamonds;
    }

     unsigned int getDiamondsOnLevel()
    {
        return diamonds_on_the_level;
    }

     std::string getType() const {
        return type_of_player;
    }
    //Setters:
    void setPosition(int new_x,int new_y)
    {
        x = new_x;
        y = new_y;
    }
};

//класс для алмазов:
class Diamond{
    private:
        int x,y;
        bool is_collected;
        std::string type ;
       
    public:
        Diamond(int x,int y,std::string type)
        {
            this->x = x;
            this->y = y;
            this->type = type;
           is_collected = false;
        }


        int getX(){
            return x;
        
        }

        int getY(){
            return y;
        }

        bool getIsCollected(){
            return is_collected;
        }

        std::string getType(){
            return type;
        }

        void collect(int x_player,int y_player,std::string type_of_player){
            if ((x== x_player) && (y==y_player)&& (type_of_player == type))
            {
                is_collected = true;
            }
            else{
                is_collected = false;
            }
        }

};


