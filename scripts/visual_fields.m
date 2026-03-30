% Dechler et al-exp-data.m
%
% Authors:      Cristian Morales & Natalia I. Márquez
% Date:         Dec-2025
% Version:      1.0
% Description:  Reconstruction of Visual fields by projecting each 
%               monocular border onto a sphere.
%
%% PART # 1: Load your Data

clear
load OD101.mat
data1=datos;
clear datos
load OD102.mat
data2=datos;
clear datos

%% Compute mean and standard error; add as many data as needed

%mean
columna2p=mean([data1(:,2) data2(:,5) ].').'; 
columna3p=mean([data1(:,3) data2(:,4) ].').';  
columna4p=mean([data1(:,3) data2(:,4) ].').';  
columna5p=mean([data1(:,2) data2(:,5) ].').';  

datamean=[columna2p columna3p columna4p columna5p];

%SE
columna2d=std([data1(:,2) data2(:,5) ].').'/sqrt(1);  
columna3d=std([data1(:,3) data2(:,4) ].').'/sqrt(1);  
columna4d=std([data1(:,3) data2(:,4) ].').'/sqrt(1);  
columna5d=std([data1(:,2) data2(:,5) ].').'/sqrt(1); 

dataSE=[columna2d columna3d columna4d columna5d];

datamean_plus=datamean+dataSE;
datamean_minus=datamean-dataSE;
datamean=[data1(:,1) datamean];
datamean_plus=[data1(:,1) datamean_plus];
datamean_minus=[data1(:,1) datamean_minus];



%%  PART# 2
C1=datamean(:,2);
C2=datamean(:,3);
C3=datamean(:,4);
C4=datamean(:,5);
v=datamean(:,1);

C1minus=datamean_minus(:,2);
C2minus=datamean_minus(:,3);
C3minus=datamean_minus(:,4);
C4minus=datamean_minus(:,5);
vminus=datamean_minus(:,1);

C1plus=datamean_plus(:,2);
C2plus=datamean_plus(:,3);
C3plus=datamean_plus(:,4);
C4plus=datamean_plus(:,5);
vplus=datamean_plus(:,1);  %

n=length(C1); 
col = zeros(n*2,4,'double');  
row = zeros(n*2,1,'double'); 

% Creates the matrices "col", "row", "colplus", and "colminus".
% In addition, it rearranges the data in the correct order to be used in the figure.

for i=1:n
    col(i,1)=max(1,90-C1(i)); 
    col(i,2)=90-C2(i);
    col(i,3)=90+C3(i);
    col(i,4)=min(180,90+C4(i));
    row(i)=v(i);
    
    
    col(n+i,1)=max(1,C2(i)-90);
    col(n+i,2)=C1(i)-90;
    col(n+i,3)=180-(C4(i)-90);
    col(n+i,4)=min(180,180-(C3(i)-90));
    row(n+i)= v(i)-180;
end

rf=flipud(row);
col2=flipud(col(:,2));
col4=flipud(col(:,4));%


n=length(C1); 
colplus = zeros(n*2,4,'double');  
rowplus = zeros(n*2,1,'double'); 
for i=1:n
    colplus(i,1)=max(1,90-C1plus(i)); 
    colplus(i,2)=90-C2plus(i);
    colplus(i,3)=90+C3plus(i);
    colplus(i,4)=min(180,90+C4plus(i));
    rowplus(i)=vplus(i);
    
    
    colplus(n+i,1)=max(1,C2plus(i)-90);
    colplus(n+i,2)=C1plus(i)-90;
    colplus(n+i,3)=180-(C4plus(i)-90);
    colplus(n+i,4)=min(180,180-(C3plus(i)-90));
    rowplus(n+i)= vplus(i)-180;
end

rfplus=flipud(rowplus); 
col2plus=flipud(colplus(:,2));
col4plus=flipud(colplus(:,4));
colminus = zeros(n*2,4,'double');  
rowmminus = zeros(n*2,1,'double'); 

for i=1:n
    colminus(i,1)=max(1,90-C1minus(i)); 
    colminus(i,2)=90-C2minus(i);
    colminus(i,3)=90+C3minus(i);
    colminus(i,4)=min(180,90+C4minus(i));
    rowminus(i)=vminus(i);   
    colminus(n+i,1)=max(1,C2minus(i)-90);
    colminus(n+i,2)=C1minus(i)-90;
    colminus(n+i,3)=180-(C4minus(i)-90);
    colminus(n+i,4)=min(180,180-(C3minus(i)-90));
    rowminus(n+i)= vminus(i)-180;
end

rfminus=flipud(rowminus); 
col2minus=(colminus(:,2));
col4minus=flipud(colminus(:,4));

%% PART # 3: The figure

close all
figure(Position= [1200 900 560 420]);
fill([row;rf],[col(:,1); col2],'r','EdgeColor',[0 0 0]);
hold on;
fill([row;rf],[col(:,3); col4],'b', 'EdgeColor',[0 0 0]);
hold on;

hold on;

fill([row;rf],[col2minus;col2plus],[0 0 0],'EdgeColor','none');
hold on;

fill([row;rf],[colminus(:,3);flipud(colplus(:,3))],[0 0 0],'EdgeColor','none');
hold on;
alpha(0.15);

%% PART # 4  
 % Remove axes from the figure and extract data to generate the CData for
 % the sphere surface.

set(gca, 'Visible', 'off');
xlabel('elevation')
cdata = print('-RGBImage','-vector', '-r600');
figure, imshow(cdata);
bw = cdata(:,:,1)<255 | cdata(:,:,2)<255 | cdata(:,:,3)<255;
imshow(bw)
[r,c] = find(bw);
cmin = min(c);
cmax = max(c);
rmin = min(r);
rmax = max(r);
imshow(cdata(rmin:rmax, cmin:cmax,:));
figure, imshow(cdata(rmin:rmax, cmin:cmax,:));
cdata=cdata(rmin:rmax, cmin:cmax,:); 


%% PART # 5: THE SPHERE

figure(Position= [1200 900 560 420]), [xs, ys, zs] = sphere;
a=surface(zs,ys,xs, 'FaceColor','texturemap','cdata',flipud(cdata),'EdgeColor',[0 0 0]);
b=surface(zs,ys,xs, 'FaceColor','texturemap','cdata',fliplr(cdata), 'EdgeColor',[0 0 0]);
axis equal tight off

rotate(b,[0,1,0],180);rotate(a,[0,1,0],180)
rotate(b,[1,0,0],180);rotate(a,[1,0,0],180)
rotate(b,[1,0,0],80);rotate(a,[1,0,0],80)
rotate(b,[0,1,0],-30);rotate(a,[0,1,0],-30)

  
