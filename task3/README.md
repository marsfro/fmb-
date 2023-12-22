### Скрипт для восстановления референсных аллелей

Dockerfile содержит все необходимые загрузки для установки и работы скрипта allele_check.py , который используется для восстановления референсных аллелей из файла FP_SNPs.txt , взятого из архива программы GRAF версии 2.4 https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/Software.cgi 

Он выполняется с помощью библиотек pysam и argparse, которые устанавливаются внутри Docker контейнера.

1. Скрипт опирается на подготовленный SNP файл, который должен пройти следующий предпроцессинг:

awk -F'\t' 'BEGIN {OFS="\t"} {print "chr"$2, $4, "rs"$1, $5, $6}' FP_SNPs.txt > output.txt

sed -e '1s/chrchromosome/CHROM/' -e '1s/GB38_position/POS/' -e '1s/rsrs#/ID/' output.txt > renamed_output.txt

grep -v '^chr23' renamed_output.txt > FP_SNPs_10k_GB38_twoAllelsFormat.tsv

В docker контейнер помещается FP_SNPs_10k_GB38_twoAllelsFormat.tsv файл

cut -f 1 FP_SNPs_10k_GB38_twoAllelsFormat.tsv | uniq | wc -l

Файл должен содердать данные об аллелях 22 хромосом

2. Предполагается, что на рабочем компьетере уже есть папка с референсным геномом версии GRCh38.d1.vd1, разбитым на 25 частей, 
если нет создайте ее и поместите в нее chr[1-22,M,X,Y].fa[.fai] файлы

mkdir -p /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/ 

3. Перед созданием Docker образа убедитесь, что в папке лежат следующие файлы:
     * Dockerfile
     * allele_check.py
     * FP_SNPs_10k_GB38_twoAllelsFormat.tsv
     * Существует директория /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/ с chr[1-22,M,X,Y].fa[.fai] файлами

4. Создайте образ Docker 

   #### docker build -t test_task3 .

5. Запустите Docker контейнер

   ####  docker run -it test_task3

6. Запустите скрипт allele_check.py внутри Docker контейнера 

    #### python3 ./allele_check.py -i FP_SNPs_10k_GB38_twoAllelsFormat.tsv -o output_FP.txt -r /ref/GRCh38.d1.vd1_mainChr/sepChrs


7. Узнайте CONTAINER_ID
Для этого в другом окне терминала наберите

    #### docker ps  

8. Заберите получившийся выходной файл и лог-файл работы скрипта.

    #### docker cp CONTAINER_ID:/py_script/output_FP.txt .
    #### docker cp CONTAINER_ID:/py_script/log_file.txt .

9. Закройте Docker контейнер

    #### exit


Описание output_FP.txt файла:
Получен файл вида:
CHROM  POS     ID      REF     ALT
chr1    1220751 rs2887286       T       C
chr1    1275912 rs6685064       C       T
chr1    2352457 rs2840528       A       G
chr1    2622185 rs3890745       T       C
chr1    3164291 rs1798246       A       C
chr1    3765267 rs1181875       T       C
chr1    3826755 rs6663840       G       A
chr1    4176922 rs4233262       C       T
chr1    4304166 rs693734        C       T

Который содержит информацию об референсном и альтернативном аллелях для всех 22 соматических хромосом. Ни для одной позиции нуклеотиды не повторяются.
