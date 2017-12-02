#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string>
#include <list>
#include <set>
#include <map>
using namespace std;

int main(int argc, char *argv[])
{
	FILE *fp, *output_map, *output_all, *output_link;
	char buf[1024];
	int i, j;
	int num;

	set<string> s;              //URLȥ�ؼ�����
	map<string, int> m;         //����URL��ID�Ĺ�ϵ
	int *index;                 //��¼ĳ��ID��ǰ���е�������
	int **graph;                //��ͼ����¼����URL������ӹ�ϵ������ͼ���ڽӱ�ʵ��

	if ((fp = fopen("url_dic_clean", "r")) == NULL)
	{
		printf("The file can not be opened.\n");//�򿪲������ɹ�
		return -1;//���������ִ��
	}

	while (fgets(buf, sizeof(buf), fp))//ÿ�ζ�ȡһ�����ݣ�ֱ����ȡʧ�ܡ� 
	{
		i = j = 0;
		while (buf[i] != ' ')
			i++;
		buf[i] = '\0';
		i++;
		while (buf[i] == ' ')
			i++;
		j = i;
		while (buf[i] != '\n')
			i++;
		buf[i] = '\0';
		string a = buf;
		string b = buf + j;
		s.insert(a);
		s.insert(b);
	}

	i = 0;
	set<string>::iterator it; //����ǰ���������������������е�����Ԫ��  
	output_map = fopen("map.txt", "w");
	for (it = s.begin(); it != s.end(); it++)
	{
		string key = *it;
		m.insert(pair<string, int>(key, i));
		fprintf(output_map, "%s %d\n", key.c_str(), i);
		i++;
	}
	fclose(output_map);

	num = i;

	index = (int *)malloc(sizeof(int) * i);//current location for each key
	memset(index, 0, sizeof(int) * i);
	graph = (int **)malloc(sizeof(int *) * i);
	memset(graph, 0, sizeof(int *) * i);
	for (j = 0; j < i; j++)
	{
		graph[j] = (int *)malloc(sizeof(int) * i);
		memset(graph[j], 0, sizeof(int) * i);
	}

	fseek(fp, 0, SEEK_SET);

	map<string, int>::iterator iter2;

	output_all = fopen("all.txt", "w");

	while (fgets(buf, sizeof(buf), fp))//ÿ�ζ�ȡһ�����ݣ�ֱ����ȡʧ�ܡ� 
	{
		i = 0;
		while (buf[i] != ' ')
			i++;
		buf[i] = '\0';
		i++;
		while (buf[i] == ' ')
			i++;
		j = i;
		while (buf[i] != '\n')
			i++;
		buf[i] = '\0';
		string a = buf;
		string b = buf + j;

		iter2 = m.find(a);
		int int_a = iter2->second;
		iter2 = m.find(b);
		int int_b = iter2->second;

		fprintf(output_all, "%d,%d\n", int_a, int_b);

		graph[int_a][index[int_a]++] = int_b;
		graph[int_b][index[int_b]++] = int_a;
	}

	fclose(output_all);

	output_link = fopen("link.txt", "w");

	for (i = 0; i < num; i++)
	{
		fprintf(output_link, "%d,", i);
		for (j = 0; j < index[i]; j++)
		{
			fprintf(output_link, "%d", graph[i][j]);
			if (j != index[i] - 1)
				fprintf(output_link, ",");
		}
		fprintf(output_link, "\n");
	}

	fclose(output_link);
	fclose(fp);//�ر��ļ��� 

	free(index);
	for (i = 0; i < num; i++)
		free(graph[i]);
	free(graph);

	return 0;
}
