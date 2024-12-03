FROM ubuntu:latest

RUN KALDI_MKL=0 && apt-get update && apt-get install -y --no-install-recommends wget bzip2 unzip xz-utils g++ make cmake git python3 python3-dev python3-websockets python3-setuptools python3-pip python3-wheel python3-cffi zlib1g-dev automake autoconf libtool pkg-config ca-certificates software-properties-common ffmpeg && rm -rf /var/lib/apt/lists/*
RUN KALDI_MKL=0 && git clone -b vosk --single-branch https://github.com/alphacep/kaldi /opt/kaldi && cd /opt/kaldi/tools && sed -i 's:status=0:exit 0:g' extras/check_dependencies.sh && sed -i 's:--enable-ngram-fsts:--enable-ngram-fsts --disable-bin:g' Makefile && make -j $(nproc) openfst cub && if [ "x$KALDI_MKL" != "x1" ] ; then extras/install_openblas_clapack.sh;  else extras/install_mkl.sh;  fi && cd /opt/kaldi/src && if [ "x$KALDI_MKL" != "x1" ] ; then ./configure --mathlib=OPENBLAS_CLAPACK --shared;  else ./configure --mathlib=MKL --shared;  fi && sed -i 's:-msse -msse2:-msse -msse2:g' kaldi.mk && sed -i 's: -O1 : -O3 :g' kaldi.mk && make -j $(nproc) online2 lm rnnlm && git clone https://github.com/alphacep/vosk-api /opt/vosk-api && cd /opt/vosk-api/src && KALDI_MKL=$KALDI_MKL KALDI_ROOT=/opt/kaldi make -j $(nproc) && cd /opt/vosk-api/python && python3 ./setup.py install && git clone https://github.com/alphacep/vosk-server /opt/vosk-server && rm -rf /opt/vosk-api/src/*.o && rm -rf /opt/kaldi && rm -rf /root/.cache  && rm -rf /var/lib/apt/lists/*
ENV MODEL_VERSION=0.22

RUN mkdir /opt/vosk-model-en  && cd /opt/vosk-model-en  && wget -q http://alphacephei.com/kaldi/models/vosk-model-en-us-${MODEL_VERSION}.zip  && unzip vosk-model-en-us-${MODEL_VERSION}.zip  && mv vosk-model-en-us-${MODEL_VERSION} model  && rm -rf vosk-model-en-us-${MODEL_VERSION}.zip

EXPOSE 7000

WORKDIR /home/
ADD ./Application/Requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

WORKDIR /home/application/

CMD python3 ./Main.py /opt/vosk-model-en/model