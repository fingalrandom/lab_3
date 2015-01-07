//longArithmetic
//argv[1][уменьшаемое] 
//argv[2][знак] 
//argv[3][вычитаемое] 
//argv[4][результат] 
//argv[5][бинарный] 
//argv[6][модуль]

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

class cur_new
{
	public:
	int znak;
	long int lenth;
	short int *mem;

	cur_new();
    ~cur_new();
};

int main(int argc, char* argv[])
{
	system("clear");
	long int maxlen;
	cur_new a;
	cur_new b;
	cur_new mod;
	cur_new rez;
	FILE *fp_a = NULL;
	FILE *fp_b = NULL;
	FILE *fp_mod = NULL;

//открываем файлы
	fp_a = fopen(argv[1], "r");
	fp_b = fopen(argv[3], "r");
//если файлы пусты, то ошибка
	if(fp_a == NULL || fp_b == NULL)
	{
		printf("ERROR");
		return 0;
	}
//открываем файл с модулем
	if(argv[6] != NULL)
	{
		fp_mod = fopen(argv[6], "r");
	}
//проверяем на отрицательность
	if(fgetc(fp_a) == '-') 
	{
		a.znak = 1;
	}
	if(fgetc(fp_b) == '-') 
	{
		b.znak = 1;
	}
//считаем длинну
	fseek(fp_a, 0, SEEK_END);
	a.lenth = ftell(fp_a) - 1 - a.znak;
	fseek(fp_a, 0, SEEK_SET);

	fseek(fp_b, 0, SEEK_END);
	b.lenth = ftell(fp_b) - 1 - b.znak;
	fseek(fp_b, 0, SEEK_SET);

	fseek(fp_mod, 0, SEEK_END);
	mod.lenth = ftell(fp_mod) - 1;
	fseek(fp_mod, 0, SEEK_SET);
//находим максимальную длинну
	if(a.lenth >= b.lenth)
	{
		maxlen = a.lenth;
	}
	else 
	{
		maxlen = b.lenth;
	}
//выделяем память под числа
	a.mem = (short *) calloc(maxlen+2, sizeof(short));
	b.mem = (short *) calloc(maxlen+2, sizeof(short));
	if(fp_mod != NULL)
	{
		mod.mem = (short *) calloc(mod.lenth + 1, sizeof(short));
	}
//ошибка выделения памяти
	if(a.mem == NULL || b.mem == NULL)
	{
		printf("ERROR");
		return 0;
	}
//записываем числа в массив
//это палево! надо исправлять
	int b5 = 48;
	if(argv[5] != NULL && strcmp(argv[5], "-b") == 0)
	{
	  b5 = 0;
	}
	fseek(fp_a, a.znak, SEEK_SET);
	fseek(fp_b, b.znak, SEEK_SET);
	for(long int i = a.lenth - 1; i >= 0; i--)
	{
	  a.mem[i] = fgetc(fp_a) - b5;
	}
	for(long int i = b.lenth - 1; i >= 0; i--)
	{
	  b.mem[i] = fgetc(fp_b) - b5;
	}
	if(fp_mod != NULL)
	{
	  for(long int i = mod.lenth - 1; i >= 0; i--)
	  {
	    mod.mem[i] = fgetc(fp_mod) - b5;
	  }
	}

	fclose(fp_a);
	fclose(fp_b);
	if(fp_mod != NULL)
	{
		fclose(fp_mod);
	}
//сложение и вычитание
	if(strcmp(argv[2],"+") == 0 || strcmp(argv[2],"-") == 0)
	{
		if(strcmp(argv[2],"-") == 0)
		{
			b.znak = (b.znak + 1) % 2;
		}
		a.znak = _sum(a, b, maxlen);
		a.lenth = maxlen;
		_save(a, "+", argv[4], argv[5]);
	}
//умножение
	if(strcmp(argv[2], "x") == 0)
	{
		if((a.znak + b.znak) == 1)
		{
		  rez.znak = 1;
		}
		else 
		{
		  rez.znak = 0;
		}
		rez.mem = (short *) calloc(a.lenth + b.lenth + 1, sizeof(short));
		rez.lenth = a.lenth + b.lenth;
		_mul(a, b, rez);
		_save(rez, "x", argv[4], argv[5]);
	}
//деление
	if(strcmp(argv[2],"/") == 0)
	{
		if((a.znak + b.znak) == 1) 
		{
		  rez.znak = 1;
		}
		else 
		{
		  rez.znak = 0;
		}
		rez.mem = (short *) calloc(maxlen+1, sizeof(short));
		rez.lenth = _div(a, b, rez, maxlen);
		_save(rez, "/", argv[4], argv[5]);
	}
//деление с остатком
	if(strcmp(argv[2],"%") == 0)
	{
		a.znak = 0;
		_mod(a, b, maxlen);
		_save(a, "%", argv[4], argv[5]);
	}
//возведение длинного числа в степень длинного числа
	if(strcmp(argv[2], "^") == 0)
	{
		if(a.znak == 1 && (b.mem[0] % 2) == 1)
		{
			rez.znak = 1;
		}
		else 
		{
			rez.znak = 0;
		}
		if(a.lenth == 1 && a.mem[0] == 0)
		{
			a.mem[0] = 1;
			a.znak = 0;
			_save(a, "^", argv[4], argv[5]);
		}
		rez.mem = (short *) calloc(2*mod.lenth + 2, sizeof(short));
		_sup(a, b, rez, mod);
		_save(rez, "^", argv[4], argv[5]);
	}
	printf("\nOperation complete\n");
	return 0;
}
//конструктор
cur_new::cur_new()
{
	lenth = 0;
	znak = 0;
	mem  = NULL;
}
//деструктор
cur_new::~cur_new()
{
	free(mem);
}
//умножение
void _mul(cur_new &a, cur_new &b, cur_new &rez)
{
	for(long int i = 0; i < rez.lenth; i++)
	{
		rez.mem[i] = 0;
	}
	for(long int i = 0; i < a.lenth; i++)
	{
		for(long int j = 0; j < b.lenth; j++)
		{
			rez.mem[i+j] += a.mem[i] * b.mem[j];
			rez.mem[i+j+1] += rez.mem[i+j] / 10;
			rez.mem[i+j] = rez.mem[i+j] % 10;
		}
	}
}
//деление
int _div(cur_new &a, cur_new &b, cur_new &rez, long int maxlen)
{
	long int i = 0;
	long int m = 0;
	int f = 0;
	while(b.lenth <= maxlen)
	{
		while(_cmp(a, b, maxlen - b.lenth) != 2)
		{
			m = maxlen - b.lenth;
			for(long int j = 0; j < b.lenth; j++)
			{
				a.mem[j+m] = a.mem[j+m] - b.mem[j] - f;
				if(a.mem[j+m] < 0)
				{
					a.mem[j+m] += 10;
					f = 1;
				}
				else 
				{
					f = 0;
				}
			}
			rez.mem[i]++;
		}
		i++;
		b.lenth++;
	}
	return i;
}
//деление с остатком
int _mod(cur_new &a, cur_new &b, long int maxlen)
{
	long int m = 0;
	int f = 0;
	if(maxlen < b.lenth)
	{
		return 0;
	}
	while(_cmp(a, b, maxlen - b.lenth) != 2)
	{
		m = maxlen - b.lenth;
		for(long int j = 0; j < b.lenth; j++)
		{
			a.mem[j+m] = a.mem[j+m] - b.mem[j] - f;
			if(a.mem[j+m] < 0)
			{
				a.mem[j+m] += 10;
				f = 1;
			}
			else 
			{
				f = 0;
			}
		}
	}
	b.lenth++;
	_mod(a, b, maxlen);
}
//сравнение
int _cmp(cur_new &a, cur_new &b, long int m)
{
	for(long int i = a.lenth - 1; i >= m; i--)
	{
		if(a.mem[i] > b.mem[i-m])
		{
			return 1;
		}
		else
		{
			return 2;
		}
	}
	return 0;
}
//сложение
int _sum(cur_new &a, cur_new &b, long int maxlen)
{
	int tmp = 0, r = 0;
	if(a.znak == 1) 
	{
		r = (10 - a.mem[0]) / 10;
		a.mem[0] = (10 - a.mem[0]) % 10;

		for(long int i = 1; i <= maxlen+1; i++)
		{
			tmp = a.mem[i];
			a.mem[i] = (9 - a.mem[i] + r) % 10;
			r = (9 - tmp + r) / 10;
		}
	}
	if(b.znak == 1) 
	{
		r = (10 - b.mem[0]) / 10;
		b.mem[0] = (10 - b.mem[0]) % 10;

		for(long int i = 1; i <= maxlen+1; i++)
		{
			tmp = b.mem[i];
			b.mem[i] = (9 - b.mem[i] + r) % 10;
			r = (9 - tmp + r) / 10;
		}
	}
	for(long int i = 0; i <= maxlen; i++)
	{
		tmp = a.mem[i];
		a.mem[i] = (a.mem[i] + b.mem[i] + r) % 10;
		r = (tmp + b.mem[i] + r) / 10;
	}
	if(a.mem[maxlen] == 9)
	{
		a.znak = 1;
		r = (10 - a.mem[0]) / 10;
		a.mem[0] = (10 - a.mem[0]) % 10;

		for(long int i = 1; i <= maxlen+1; i++)
		{
			tmp = a.mem[i];
			a.mem[i] = (9 - a.mem[i] + r) % 10;
			r = (9 - tmp + r) / 10;
		}
	}
	else 
	{
		a.znak = 0;
	}
	return a.znak;
}
int _sup(cur_new &a, cur_new &b, cur_new &rez, cur_new &mod)
{
	long int tmp;
	cur_new p, q;
    p.lenth = mod.lenth;
    tmp = p.lenth;
	p.mem = (short *) calloc(2*mod.lenth + 2, sizeof(short));
    q.mem = (short *) calloc(2*mod.lenth + 2, sizeof(short));
	for(long int i = 0; i < mod.lenth + 1; i++)
	{
		p.mem[i] = mod.mem[i];
	}
    _mod(a, p, a.lenth);
    p.lenth = tmp;
	
	for(long int i = 0; i < a.lenth + 1; i++)
	{
		rez.mem[i] = a.mem[i];
	}
    rez.lenth = p.lenth;
    q.lenth = 2 * p.lenth;

    while(_sup_sup(b) == 1)
    {
        rez.lenth = p.lenth;
        _mul(rez, a, q);
		for(long int i = 0; i < q.lenth + 1; i++)
		{
			rez.mem[i] = q.mem[i];
		}
        rez.lenth = q.lenth;
        tmp = p.lenth;
        _mod(rez, p, rez.lenth);
        p.lenth = tmp;
    }
    rez.lenth = p.lenth;
	return 0;
}
int _sup_sup(cur_new &b)
{
	int f = 0;
	b.mem[0] = b.mem[0] - 1;
	for(long int i = 0; i < b.lenth + 1; i++)
	{
		b.mem[i] -= f;
		if(b.mem[i] >= 0)
		{
			f = 0;
		}
		else 
		{
			b.mem[i] += 10;
			f = 1;
		}
	}
	for(long int i = 0; i < b.lenth + 1; i++)
	{
		if(b.mem[i] != 0)
		{
			return 1;
		}
	}
	return 0;
}
//запись в файл
int _save(cur_new &rez, const char *oper, char *filerez, char *bin)
{
	char ch;
	long int t;
	int _const;
	FILE *fp;
	if(strcmp(bin, "-b") == 0)
	{
		if(filerez == NULL)
		{
			filerez = (char*) "rez.bin";
		}
		fp = fopen(filerez, "wb");
		_const = 48;
	}
	else
	{
		if(filerez == NULL)
		{
			filerez = (char*) "rez";
		}
		fp = fopen(filerez, "w");
		_const = 0;
	}

	if(strcmp(oper, "/") == 0)
	{
		t = 0;
		for(long int i = 0; i  < rez.lenth; i++)
		{
			if(rez.mem[i] == 0)
			{
				t++;
			}
		}
		else 
		{
			break;
		}
		if(t == rez.lenth)
		{
			t--;
			rez.znak = 0;
		}
		if(rez.znak == 1)
		{
			fprintf(fp, "-");
		}
		for(long int i = t; i < rez.lenth; i++)
		{
			ch = rez.mem[i] + 48 - _const;
			fprintf(fp, "%c", ch);
		}
		return 0;
	}

	t = rez.lenth;
	for(long int i = rez.lenth; i > 0; i--)
	{
		if(rez.mem[i] == 0)
		{
			t--;
		}
	}
	else 
	{
		break;
	}
	if(t == 0) 
	{
		rez.znak = 0;
	}
	if(rez.znak == 1) 
	{
		fprintf(fp, "-");
	}
	for(long int i = t; i >= 0; i--)
	{
		ch = rez.mem[i] + 48 - _const;
		fprintf(fp, "%c", ch);
	}
	return 0;
}
