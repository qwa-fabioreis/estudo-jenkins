# Passo a Passo para compilar: ccvwrapper.c

### **AMBIENTE**

> Todo esse processo de compilação do ```ccvwrapper.c``` foi implementado e testado no WLS2 com Ubuntu-20.04


----

Contexto de alguns arquivos importantes:

* ```ccvwrapper.i```      - Arquivo de interface para o SWIG. São instruções para o swig realizar a transpilação de C para Python e conversão de tipos entre C e Python.
* ```ccvwrapper.c```      - Arquivo que rebece os bytes da imagem e envia para o algoritmo SWT da lib ccv, que ira encontrar as coordenadas dos blocos de texto da imagem e retornar uma lista com todas as coordenadas em um array de int. (A correção do shape da desta lista é feito assim que o wrapper retorna o resultado no identify_text_areas no block_finder.py)
* ```ccvwrapper.h```      - Arquivo de cabeçalho com o protótipo da função que é utilizado no ccvwrapper.c
* ```ccvwrapper.py```     - Arquivo python que contem toda a inteface pronta para executar a compilação do arquivo ccvwrapper.c
* ```ccvwrapper_wrap.c``` - Arquivo que faz a comunicação entre Python e o executavel em C já compilado.
* ```ccvwrapper.so```     - Este arquivo é o que seria o ccvwrapper.c já "compilado" para ser utilizado no Python. É este arquivo que o ccvwrapper.py chama nas primeiras linhas de import.

----

### **OBS**
Para todos os comandos bash que serão apresentados, é necessários que esteja dentro da pasta:

```
/premier-pet-project/premier-pet-core/app/lib/ccvwrapper/
```

----

## **PASSO A PASSO:**

<br>

> * **1º Passo:** Baixar a versão estável do liuliu/cvv para dentro do diretorio: 
```console
$ wget https://github.com/liuliu/ccv/tarball/stable
```
<br>

> * **2º Passo:** Renomear o arquivo baixado de: ***stable*** para ***libccv**. (Deve-se usar esse nome para facilitar a indicação do arquivo para compilação, logo mais abaixo)
```
$ mv stable libccv.tar
```
<br>

> * **3º Passo:** Extrair os arquivos
```
$ tar -xf libccv.tar
```
<br>

> * **4º Passo:** Renomear a pasta com os arquivos extraidos de: ***liuliu-ccv-07fc691*** para ***libccv*** (Como dito anteriormente, irá fazer referencia aos arquivos de compilacao).
```
$ mv liuliu-ccv-07fc691 libccv
```
##### Caso tenha algum problema de permissão com a seguinte menssagem: ```mv: cannot move 'liuliu-ccv-07fc691' to 'libccv'```, provavelmente é por conta do Visual Studio Code estar aberto ou qualquer programa que tenha alguma relação direta ou indireta com essa pasta.
<br>

> * **5º Passo:** Excluir o arquivo baixado ***libccv.tar*** pois não será mais necessário.
```
$ rm libccv.tar
```

----

### **Este Passo não necessário - Mas se por algum motivo precisar**


> Caso precise fazer a compilação do projeto na pasta lib:

```
$ cd libccv/lib/
$ ./configure && make 
```

> Ira gera um arquivo ***libccv.a***

----

## **INSTALAÇÂO DE DEPENDÊNCIAS:**

<br>

> **Gerador de codigo SWIG**
```
$ sudo apt install swig
```

<br>

> **Dependencia do ccv que podem ser necessarias**
```
$ sudo apt install libjpeg-dev libpng-dev
```

<br>

> **Evita o problema do ```#include <Python.h>``` no ccvwrapper_wrap.c** quando for compilar.
```
$ sudo apt install python3-dev
```

----


## **REPETIR A PARTIR DESSE PONTO, CASO TENHA SIDO FEITO ALGUMA ALTERACAO NO ARQUIVO ccvwrapper.c**

----

> * **6º Passo:** - Gerar os wrappers com SWIG - (Ira gerar os arquivos ***ccvwrapper.py*** e ***ccvwrapper_wrap.c***)
```
$ swig -python ccvwrapper.i
```
<br>


> * **7º Passo:** Compilar todos os arquivo necessarios para o wrapper - (Deve mostar apenas alguns warnings)

##### **OBS:** Observar essa flag no final da linha de execução abaixo: ```-I/usr/include/python3.8``` - Cheque se a versão do python no final da flag é a mesma instalada no sistema. Quando a compilação do **ccvwrapper_wrap.c** é feita, sempre deve-se garantir que o ```#include <Python.h>``` é da versão que o app principal será executado, no caso **premier-pet-core** versão 3.8 do Python
```
$ gcc -fpic -c ccvwrapper.c ccvwrapper_wrap.c ./libccv/lib/ccv_algebra.c ./libccv/lib/ccv_basic.c ./libccv/lib/ccv_cache.c ./libccv/lib/ccv_classic.c ./libccv/lib/ccv_io.c ./libccv/lib/ccv_memory.c ./libccv/lib/ccv_output.c ./libccv/lib/ccv_resample.c ./libccv/lib/ccv_sift.c ./libccv/lib/ccv_swt.c ./libccv/lib/ccv_transform.c ./libccv/lib/ccv_util.c ./libccv/lib/3rdparty/sha1/sha1.c -I/usr/include/python3.8
```
##### Durante este processo de compilação do ```gcc```, irá gerar vários warning, mas não tem nenhuma influência na compilação e na execução do wrapper.
<br>


> * **8º Passo:** Criar linker de todos os arquivo ```.o``` para poder gerar ```_ccvwrapper.so``` que é o arquivo principal de todo esse processo.
```
$ ld -shared ccvwrapper.o ccvwrapper_wrap.o ccv_algebra.o ccv_basic.o ccv_cache.o ccv_classic.o ccv_io.o ccv_memory.o ccv_output.o ccv_resample.o ccv_sift.o ccv_swt.o ccv_transform.o ccv_util.o sha1.o -ljpeg -o _ccvwrapper.so
```
<br>


> * **9º Passo:** Depois que for gerado o arquivo ```_ccvwrapper.so```, não é mais necessario do resto dos arquivo (.o). Então é só executar o comando abaixo para excluir todos eles.
```
$ rm -v ccv_algebra.o ccv_basic.o ccv_cache.o ccv_classic.o ccv_io.o ccv_memory.o ccv_output.o ccv_resample.o ccv_sift.o ccv_swt.o ccv_transform.o ccv_util.o sha1.o
```
<br>

> **Caso precise fazer mais alterações no ```ccvwrapper.c```, é só repetir apatir do passo 6.**
----

### Caso já tenha feito todas as alterações e não precise mais compilar nada, execute o comando para excluir a pasta libccv:
```
$ rm -rv libccv/
```


# **OBS:** Se atente para não enviar a pasta ```libccv``` e os arquivos desnecessarios com extensão ```.o``` para o repositório remoto do projeto!

<br>

----

### **Referencias**:

- https://zablo.net/blog/post/stroke-width-transform-swt-python/
- https://github.com/liuliu/ccv/
- https://libccv.org/
