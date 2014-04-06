function fpsc
%文本聚类
%  高质量文本的频繁项集进行聚类
%  聚类的方法采用谱聚类

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  Huang Jimin
%  2014-3-28

%%%%% Baseline1 Step 2

%读取数据
data=load('vsm1.txt');
%聚类数目
cluster_number=9;
n=size(data,1);
node_matrix = zeros(n, n);
degree_matrix = zeros(n, n); 
%计算相似度矩阵
for i = 1 : n
    for j = i : n
        node_matrix(i, j) = pdist2(data(i, :), data(j, :), 'Euclidean');
        node_matrix(j, i) = node_matrix(i, j);
    end
    degree_matrix(i, i) = sum(node_matrix(i, :));
end
%拉普拉斯矩阵计算并规范化
L_matrix = degree_matrix - node_matrix; 
for i = 1 : n
    degree_matrix(i, i) = degree_matrix(i, i) ^ (-1 / 2);
end

L_matrix = degree_matrix * L_matrix * degree_matrix;
%计算特征值与特征向量
[e_vectors,e_values]=eig(L_matrix);
%选取前k个最大的特征值
select_E_vectors = e_vectors(:, 1 : cluster_number);
norm_select_E_vectors = zeros(n, cluster_number);

for i = 1 : n
    for j = 1 : cluster_number
        norm_select_E_vectors(i, j) = select_E_vectors(i, j) / (sum(select_E_vectors(i, :) .^ 2) ^ (0.5));
    end
end
%kmeans聚类
[labels, center, sumD, D] = kmeans(norm_select_E_vectors, cluster_number);
%计算向量与对应聚类中心的平均距离
cen_num = zeros(cluster_number,1);
for i = 1 : n
    cen_num(labels(i)) = cen_num(labels(i))+1;
end
for i = 1 : cluster_number
    sumD(i) = sumD(i) / cen_num(i);
end
sums= sum(sumD) / cluster_number;
%计算与聚类中心最接近的向量
mins = zeros(cluster_number,1)
for i = 1 : cluster_number
    temp=min(D(:,i));
    mins(i)=find(D(:,i)==temp);
end
%计算聚类中心之间的平均距离
distance=zeros(cluster_number,cluster_number);
for i= 1 : cluster_number
    for j= i: cluster_number
        distance(i,j)=pdist2(center(i,:), center(j, :), 'Euclidean');
    end
end
distances=sum(sum(distance)) / (cluster_number *(cluster_number-1) / 2);
%计算比值
force=sums/distances;
%输出文件
dlmwrite('s-result-centroids.txt', mins);
dlmwrite('s-result-labels.txt', labels);  % 最后只需该文件
dlmwrite('s-result-c.txt', sums);
dlmwrite('s-result-s.txt', distances);
dlmwrite('s-result-cs.txt', force);
end