#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <algorithm>
#include <dirent.h> 

#define MAXN 30
#define MAXL 100
#define MAXFILE 50
#define MAXCLAUSE 2000

typedef struct cat {
    char code[MAXL];
    char alias[MAXL];
} cat;

cat cats[MAXN];
char types[MAXN][MAXFILE];
char rev_clause[MAXCLAUSE];

bool cat_cmp(cat a, cat b) {
    return strcmp(a.alias, b.alias) < 0;
}

inline bool is_endline(char x) {
    return x == '\n' || x == '\r';
}

inline bool is_inputfile(char *x) {
    int l = strlen(x) - 5;
    if (l > 0 && strcmp(&x[l], ".type") == 0)
    {
        x[l] = '\0';
        return true;
    }
    return false;
}

void analyzeType(char *cat_type);

int main(int argc, const char *argv[])
{
    if (argc > 1)
        freopen(argv[1], "w", stdout);
    printf("var types = new Array();\nvar aliases = new Array();\n");
    DIR *d;
    struct dirent *dir;
    int n = 0;
    d = opendir(".");
    if (d)
    {
        while ((dir = readdir(d)) != NULL)
            if (is_inputfile(dir->d_name))
                strcpy(types[n++], dir->d_name); //analyzeType(dir->d_name);

        closedir(d);
    }
    qsort(types, n, MAXFILE, (int (*)(const void *, const void *))strcmp);
    strcpy(rev_clause, "var typeNames = new Array();\n");
    for (int i = 0 ; i < n ; ++i)
        analyzeType(types[i]);
    printf("%s", rev_clause);
    if (argc > 1)
        fclose(stdout);
    return 0;
}

void analyzeType(char *cat_type)
{
    memset(cats, 0, sizeof(cats));
    char cFile[MAXFILE];
    sprintf(cFile, "%s.type", cat_type);
    FILE *fin = fopen(cFile, "r");
    int n = 0;
    while (fgets(cats[n].code, MAXL, fin) != NULL)
    {
        if (fgets(cats[n].alias, MAXL, fin) != NULL)
        {
            while (is_endline(cats[n].code[strlen(cats[n].code) - 1]))
                cats[n].code[strlen(cats[n].code) - 1] = '\0';
            while (is_endline(cats[n].alias[strlen(cats[n].alias) - 1]))
                cats[n].alias[strlen(cats[n].alias) - 1] = '\0';
            n++;
        }
    }
    std::sort(cats, cats + n, cat_cmp);
    printf("types[\"%s\"] = new Array(", cat_type);
    char prefix[3];
    prefix[0] = '\0';
    for (int i = 0 ; i < n ; i++)
    {
        printf("%s\"%s\"", prefix, cats[i].code);
        sprintf(rev_clause, "%stypeNames[\"%s\"] = \"%s\";\n", rev_clause, cats[i].code, cat_type);
        strcpy(prefix, ", ");
    }
    printf(");\naliases[\"%s\"] = new Array(", cat_type);
    prefix[0] = '\0';
    for (int i = 0 ; i < n ; i++)
    {
        printf("%s\"%s\"", prefix, cats[i].alias);
        strcpy(prefix, ", ");
    }
    printf(");\n");
    fclose(fin);
}
