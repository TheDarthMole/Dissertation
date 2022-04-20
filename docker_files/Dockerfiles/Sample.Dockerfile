FROM maven

RUN git clone https://github.com/tecnico-distsys/example_junit.git /source
WORKDIR /source
RUN mvn compile
RUN mvn test
