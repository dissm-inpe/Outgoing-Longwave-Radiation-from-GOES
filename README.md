# Outgoing-Longwave-Radiation-from-GOES
Modelo de Radiação de Onda Longa Emergente (OLR) a partir de observações do satélite GOES.

Este repositório contém a implementação do modelo operacional de estimativa da OLR desenvolvido no INPE a partir das observações do satélite GOES-19.

O sistema processa dados de temperatura de brilho do sensor ABI, realizando a conversão para OLR por meio de uma parametrização empírica, gerando produtos regulares para a América do Sul.

Principais funcionalidades:
* Leitura dos dados do GOES-19 ABI;
* Conversão de temperatura de brilho em OLR;
* Reprojeção dos dados da geometria do satélite para uma grade regular latitude-longitude;
* Preenchimento de lacunas espaciais;
* Geração de produtos de OLR com resolução temporal de 3 horas;
* Cálculo de médias diárias;
* Exportação em formatos binário, imagem e NetCDF;
* Produção operacional para monitoramento climático e meteorológico.
* Domínio espacial

Os produtos são gerados em uma grade regular de 0,04° cobrindo a América do Sul:

Latitude: 50°S a 22°N
Longitude: 100°W a 28°W

Ceballos, J.C., W.F.A. Lima, J.M. Souza. Outgoing longwave radiation at the top of the atmosphere: Preliminary assessment using GOES-8 Imager data. Revista Brasileira de Geofísica, v. 21, p. 53-64, 2003.


Código original em python desenvolvido por: Márcio Brito.
