FROM ubuntu:latest

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y openjdk-8-jdk wget python3 python3-pip

# Установка Python пакетов
RUN pip3 install pyspark jupyter

# Скачивание и распаковка Apache Spark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
RUN tar -xvzf spark-3.5.0-bin-hadoop3.tgz
RUN mv spark-3.5.0-bin-hadoop3 /spark

# Установка PostgreSQL JDBC драйвера
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.25.jar
RUN mv postgresql-42.2.25.jar /spark/jars

# Установка переменных среды
# /usr/lib/jvm/java-8-openjdk-arm64 зависит от железа, в данном с лучае АРМ
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-arm64  
ENV SPARK_HOME /spark
ENV PATH $PATH:$SPARK_HOME/bin

# Установка рабочей директории
WORKDIR /spark

# Открываем порт для Jupyter Notebook
EXPOSE 8888

# Запуск Jupyter Notebook
CMD ["jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--NotebookApp.token=''"]
