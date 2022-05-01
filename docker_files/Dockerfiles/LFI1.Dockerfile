FROM maven

COPY ./Java/LFI/FileReader /source
WORKDIR /source
RUN mvn compile
# || true because the tests SHOULD fail initially, but
# docker thinks that's an unexpected error
# They need to make the fixes in the app
RUN mvn test || true
