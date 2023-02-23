#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Grade assigned to each Grade point
char GRADE[] = {'A','B','C','D','E', 'F'};

// Point assigned to each Grade
int POINTS[] = {5, 4, 3, 2, 1, 0};
// Courses have code, grade, total score, unit and gp
typedef struct
{
    char *code;
    char *grade;
    int total;
    int unit;
    int gp;
}
course;


int main(int argc, char *argv[])
{
    // Instructs user on usage format
    if (argc < 2)
    {
        printf("Usage: CGPA [course code ....]\n");
        return 1;
    }
    // Array of course
    course courses[argc - 1];
    printf("Your Courses are: \n\n");
    // Assign each course codes to course array
    for (int i = 0; i < argc - 1; i++)
    {
        courses[i].code = argv[i + 1];
    }
    // Get the length of Course
    int length = sizeof(courses) / sizeof(courses[0]);

    // Keep Querying for Total and Unit
    for (int i = 0; i < length; i++)
    {
        int total = 0;
        int unit = 0;
        printf("Enter the Total score of %s: ", courses[i].code);
        scanf("%i", &total);
        printf("Enter the Unit of %s: ", courses[i].code);
        scanf("%i", &unit);
        if ((total > 0 || total == 0) && (total < 100 || total == 100))
        {
            courses[i].total = total;
        }
        else
        {
            printf("Exam total must be between 0 and 100 (both inclusive)!!\n");
            return 1;
        }
        if (unit > 0 && (unit < 12 || unit == 12))
        {
            courses[i].unit = unit;
        }
        else
        {
            printf("Course unit must be between 1 and 12 (both inclusive)!!\n");
            return 1;
        }
    }

    for (int i = 0; i < length; i++)
    {
        printf("No.%i: %s\n",i + 1, courses[i].code);
    }

    return 0;
}

// void grade_assign()
// {
//     for (int i = 0; i < length; i++)
//     {
//         if (courses[i].total == 70 || courses[i].total >)
//     }
// }

// void gp_assign(char grade, int gp)
// {
//     for (int i = 0; i < length; i++)
//     {

//     }
// }