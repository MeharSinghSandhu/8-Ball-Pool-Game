#include "phylib.h"



                                                        //PART 1

// Allocaton for STILL BALL
phylib_object *phylib_new_still_ball( unsigned char number,phylib_coord *pos ){

    phylib_object *obj =  malloc(sizeof(phylib_object));

    if (obj == NULL){
        return NULL;
    }

    obj->type = PHYLIB_STILL_BALL;
    obj->obj.still_ball.number = number;
    obj->obj.still_ball.pos.x = pos->x;
    obj->obj.still_ball.pos.y = pos->y;

    return obj;
}



//Allocation for ROLLING BALL
phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc ){

    phylib_object *obj = malloc(sizeof(phylib_object));

    if (obj == NULL){
        return NULL;
    }

    obj->type = PHYLIB_ROLLING_BALL;
    obj->obj.rolling_ball.number = number;
    obj->obj.rolling_ball.pos.x = pos->x;
    obj->obj.rolling_ball.pos.y = pos->y;
    obj->obj.rolling_ball.vel.x = vel->x;
    obj->obj.rolling_ball.vel.y = vel->y;
    obj->obj.rolling_ball.acc.x = acc->x;
    obj->obj.rolling_ball.acc.y = acc->y;

    return obj;
}




//Allocation for HOLE
phylib_object *phylib_new_hole( phylib_coord *pos ){

    phylib_object *obj = malloc(sizeof(phylib_object));

    if (obj == NULL){
        return NULL;
    }

    obj->type = PHYLIB_HOLE;
    obj->obj.hole.pos.x = pos->x;
    obj->obj.hole.pos.y = pos->y;

    return obj;   

}



//Allocation for HORIZONTAL CUSHION
phylib_object *phylib_new_hcushion( double y ){

    phylib_object *obj = malloc(sizeof(phylib_object));

    if (obj == NULL){
        return NULL;
    }

    obj->type = PHYLIB_HCUSHION;
    obj->obj.hcushion.y = y;

    return obj;    

}



//Allocation for VERTICAL CUSHION
phylib_object *phylib_new_vcushion( double x ){

    phylib_object *obj = malloc(sizeof(phylib_object));

    if (obj == NULL){
        return NULL;
    }

    obj->type = PHYLIB_VCUSHION;
    obj->obj.vcushion.x = x;

    return obj;    

}


//TABLE 
phylib_table *phylib_new_table( void ){

    phylib_table *table = malloc(sizeof(phylib_table));
    
    if(table == NULL){
        return NULL;
    }

    table->time = 0.0;          //set the time to 0

    //horizontal cushions
    table->object[0] = phylib_new_hcushion(0.0);            
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);  

    //vertical cushions
    table->object[2] = phylib_new_vcushion(0.0);            
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //Adding HOLES
    table->object[4] = phylib_new_hole(&(phylib_coord){0.0,0.0}); //TOP LEFT
    table->object[5] = phylib_new_hole(&(phylib_coord){0.0,PHYLIB_TABLE_WIDTH}); //TOP RIGHT
    table->object[6] = phylib_new_hole(&(phylib_coord){0.0,PHYLIB_TABLE_LENGTH}); //BOTTOM LEFT
    table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH,0.0}); //BOTTOM RIGHT
    table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH,PHYLIB_TABLE_WIDTH}); //MIDWAY LEFT
    table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH,PHYLIB_TABLE_LENGTH}); //MIDWAY RIGHT

    for(int i =10; i < PHYLIB_MAX_OBJECTS ; i++ ){
        table->object[i] = NULL ;
    }

    return table; //Return the pointer to new table     
}


                                                        //PART 2


// COPY OBJECT
void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    if ( *src == NULL) {
        *dest = NULL; // If src is NULL, set dest to NULL
    } 
    else {
        *dest = malloc(sizeof(phylib_object)); // Allocate memory for the new object
        if (*dest != NULL) {
            memcpy(*dest, *src, sizeof(phylib_object)); // Copy the contents from src to dest
        }
    }
}


//COPY TABLE
phylib_table *phylib_copy_table(phylib_table *table) {
    if (table == NULL) {
        return NULL; // If the original table is NULL, return NULL
    }

    // Allocate memory for the new table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_table == NULL) {
        return NULL; // If memory allocation fails, return NULL
    }

    // Copy the time value
    new_table->time = table->time;

    // Initialize all object pointers to NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    // Iterate over the object array and copy each object using phylib_copy_object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            phylib_copy_object(&(new_table->object[i]), &(table->object[i]));
        }
    }

    return new_table; // Return the pointer to the new table
}





//ADD OBJECT
void phylib_add_object( phylib_table *table, phylib_object *object ){
    if(table == NULL || object == NULL){
        return ;
    }

    for(int i = 0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            break;
        }
    }
}


//FREE TABLE
void phylib_free_table( phylib_table *table ){
    for(int i = 0 ; i<PHYLIB_MAX_OBJECTS ; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);
            table->object[i] = NULL;
        }    
    }
    free(table);
}


//DIFFERENCE
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord res;

    res.x = c1.x - c2.x;
    res.y = c1.y - c2.y;

    return res;
}


//LENGTH OF VECTOR COORDINATE
double phylib_length( phylib_coord c ){
    return sqrt(c.x * c.x + c.y * c.y); 
}


//DOT PRODUCT
double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return a.x * b.x + a.y * b.y; 
}


//FINDING DISTANCE 
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    if(obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL){
        return -1;
    }
    double distance , dx , dy;
    switch (obj2->type) {
        case PHYLIB_STILL_BALL:
            dx = obj1->obj.rolling_ball.pos.x - obj2->obj.still_ball.pos.x;
            dy = obj1->obj.rolling_ball.pos.y - obj2->obj.still_ball.pos.y;
            distance = sqrt(dx * dx + dy * dy) - PHYLIB_BALL_DIAMETER;  
            break;
        case PHYLIB_ROLLING_BALL:
            dx = obj1->obj.rolling_ball.pos.x - obj2->obj.rolling_ball.pos.x;
            dy = obj1->obj.rolling_ball.pos.y - obj2->obj.rolling_ball.pos.y;
            distance = sqrt(dx * dx + dy * dy) - PHYLIB_BALL_DIAMETER;  
            break;

        case PHYLIB_HOLE:
            dx = obj1->obj.rolling_ball.pos.x - obj2->obj.hole.pos.x;
            dy = obj1->obj.rolling_ball.pos.y - obj2->obj.hole.pos.y;
            distance = sqrt(dx * dx + dy * dy) - PHYLIB_HOLE_RADIUS;
            break;

        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;

        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;

        default:
            return -1;
    }

    return distance ; // Distance cannot be negative
}


                                                            //PART 3 



//ROLL PHYSICS
void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    // Check if both objects are rolling balls, otherwise do nothing
    if (new == NULL || old == NULL || 
        new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    // Calculate new position using the kinematic equation: p = p1 + v1*t + 0.5*a1*t^2
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + 
                                  old->obj.rolling_ball.vel.x * time + 
                                  0.5 * old->obj.rolling_ball.acc.x * time * time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + 
                                  old->obj.rolling_ball.vel.y * time + 
                                  0.5 * old->obj.rolling_ball.acc.y * time * time;

    // Calculate new velocity using the equation: v = v1 + a1*t
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + 
                                  old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + 
                                  old->obj.rolling_ball.acc.y * time;

    // If the velocity changes sign (indicating a change in direction), set it and the acceleration to zero
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0) {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }
    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0) {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }
}


unsigned char phylib_stopped(phylib_object *object) {
    if (object == NULL || object->type != PHYLIB_ROLLING_BALL) {
        return 0; // Return 0 if object is NULL or not a ROLLING_BALL
    }

    // Calculate the speed of the ball
    double speed = phylib_length(object->obj.rolling_ball.vel);

    // Check if the ball has stopped
    if (speed < PHYLIB_VEL_EPSILON) {
        // Convert the rolling ball to a still ball
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        // The velocity and acceleration are not transferred and can be disregarded
        return 1; // Return 1 as the ball has been converted to STILL_BALL
    }

    return 0; // Return 0 if the ball has not stopped
}


void phylib_bounce(phylib_object **a, phylib_object **b) {

    // Ensure a is a rolling ball
    if ((*a)->type != PHYLIB_ROLLING_BALL) return;

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;

        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;

        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break; // Early return to avoid dereferencing a NULL pointer

        case PHYLIB_STILL_BALL:
            // Convert b to a rolling ball with zero velocity and acceleration
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            // Fall through to ROLLING_BALL case

        case PHYLIB_ROLLING_BALL:{
            phylib_coord r_ab;
            phylib_coord v_rel;

        // Assign the values to r_ab
            r_ab.x = (*a)->obj.rolling_ball.pos.x - (*b)->obj.rolling_ball.pos.x;
            r_ab.y = (*a)->obj.rolling_ball.pos.y - (*b)->obj.rolling_ball.pos.y;

        // Now assign the values to v_rel
            v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
            v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;

            // Calculate the length of the relative position vector (r_ab_len) and the normal vector (n)
            double r_ab_len = sqrt(r_ab.x * r_ab.x + r_ab.y * r_ab.y);
            phylib_coord n = { r_ab.x / r_ab_len, r_ab.y / r_ab_len };

            // Calculate the relative velocity along n (v_rel_n)
            double v_rel_n = v_rel.x * n.x + v_rel.y * n.y;

            
            // Update the velocities of a and b
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

                // Update the acceleration of a based on its new velocity
            double speed_a = sqrt((*a)->obj.rolling_ball.vel.x * (*a)->obj.rolling_ball.vel.x + 
                                    (*a)->obj.rolling_ball.vel.y * (*a)->obj.rolling_ball.vel.y);
            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            }

                // Update the acceleration of b based on its new velocity
            double speed_b = sqrt((*b)->obj.rolling_ball.vel.x * (*b)->obj.rolling_ball.vel.x + 
                                (*b)->obj.rolling_ball.vel.y * (*b)->obj.rolling_ball.vel.y);
            if (speed_b > PHYLIB_VEL_EPSILON) {
                    (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
            } 
            
        }
        
            break;

        default:
            // If object b's type is unknown, do nothing
            break;
    }
}



unsigned char phylib_rolling(phylib_table *t) {
    if (t == NULL) {
        return 0; // If the table is NULL, return 0
    }

    unsigned char count = 0;

    // Iterate over the objects in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        // Check if the object exists and is a rolling ball
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count; // Return the number of rolling balls
}



phylib_table *phylib_segment(phylib_table *table) {

    if (table == NULL || phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *new_table = phylib_copy_table(table);
    if (new_table == NULL) {
        return NULL;
    }

    double time_increment = PHYLIB_SIM_RATE;

    while (time_increment< PHYLIB_MAX_TIME) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {
               
                // Roll the ball
                phylib_roll(new_table->object[i], table->object[i], time_increment);
            }
        }
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {

                // Check for collisions with other objects
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (i != j && new_table->object[j] != NULL) {
                        double distance = phylib_distance(new_table->object[i], new_table->object[j]);
                        if (distance < 0.0) {
                            // Collision detected, apply bounce
                            phylib_bounce(&(new_table->object[i]), &(new_table->object[j]));
                            new_table->time += time_increment;
                            return new_table;
                        }
                    }
                }

                // Check if the ball has stopped
                if (phylib_stopped(new_table->object[i])) {
                    new_table->time += time_increment;
                    return new_table;
                }
 
            }
        }

        time_increment += PHYLIB_SIM_RATE;
         // Update the table time
    }
    new_table->time += time_increment;

    return new_table;
}

char *phylib_object_string( phylib_object *object )
{
static char string[80];
if (object==NULL)
{
snprintf( string, 80, "NULL;" );
return string;
}
switch (object->type)
{
case PHYLIB_STILL_BALL:
snprintf( string, 80,
"STILL_BALL (%d,%6.1lf,%6.1lf)",
object->obj.still_ball.number,
object->obj.still_ball.pos.x,
object->obj.still_ball.pos.y );
break;
case PHYLIB_ROLLING_BALL:
snprintf( string, 80,
"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
object->obj.rolling_ball.number,
object->obj.rolling_ball.pos.x,
object->obj.rolling_ball.pos.y,
object->obj.rolling_ball.vel.x,
object->obj.rolling_ball.vel.y,
object->obj.rolling_ball.acc.x,
object->obj.rolling_ball.acc.y );
break;
case PHYLIB_HOLE:
snprintf( string, 80,
"HOLE (%6.1lf,%6.1lf)",
object->obj.hole.pos.x,
object->obj.hole.pos.y );
break;
case PHYLIB_HCUSHION:
snprintf( string, 80,
"HCUSHION (%6.1lf)",
object->obj.hcushion.y );
break;
case PHYLIB_VCUSHION:
snprintf( string, 80,
"VCUSHION (%6.1lf)",
object->obj.vcushion.x );
break;
}
return string;
}



