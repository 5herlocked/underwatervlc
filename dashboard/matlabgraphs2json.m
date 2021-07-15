clc;    % Clear the command window.
close all;  % Close all figures (except those of imtool.)
imtool close all;  % Close all imtool figures.
clear;  % Erase all existing variables.
workspace;  % Make sure the workspace panel is showing.
fontSize = 22;
% --------------------------------------------------PATH-------------------------------------------------


path='/Applications/XAMPP/xamppfiles/htdocs/underwater-website/video-data/50Hz_100fps_Vertical.mp4';


% --------------------------------------------------------------------------------------------------------



 
tic % for measuring runtime



videoObject = VideoReader(path);
% Determine how many frames there are.
    numberOfFrames = videoObject.NumFrames;
%   numberOfFrames = 10000; % <-------------------------------- For changing number of frames
    
 
    
    
% Creating Matrices 
meanGrayLevels = zeros(numberOfFrames, 1);
meanRedLevels = zeros(numberOfFrames, 1);
meanGreenLevels = zeros(numberOfFrames, 1);
meanBlueLevels = zeros(numberOfFrames, 1);
bits = zeros(numberOfFrames, 1);
new_bits = zeros(numberOfFrames,1);
thresholdlist = [];


    
% fprintf(fid, sprintf('{\"blue\": %s}', test))
    
%==============================ROI==========================================

thisFrame = read(videoObject, 500);
imshow(thisFrame, []);
axis on;
set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.  
h_rect = drawrectangle('Color',[1 1 1]);% this helps us to draw over the frame
% Rectangle position is given as [x, y, width, height]
pos_rect = h_rect.Position();
% Round off so the coordinates can be used as indices
pos_rect = round(pos_rect);
close(gcf)

    
    
    
%---------------------------TRANSMISSION-----------------------------    

transmitted_stream = '1111000000110010001001111101001101010111101100001001010111110000111010001111111111001110100100011111111110110000011001110000011010011101000010111110111001110111101001110010111010110000101101001111001000001110010110010001001111000110000010000001100000100001001011010010001000001001001010000100101111111111000111101111001010001101011111000010010011111010100001000001100100000001011000011011000100100000110001101010001100001100110111000110110010101011100001111101011011001010101101010000100101101010110101110001001101001010010001110000010010111010011001101100010100001010100110111011111101000110000001011011011011011110101100100011000000011011010110110001001011110000000100110110111110000110110100110100000100101001100010110011101001001000101100111100001100000011000001111010100001101101010111111101100001101100001110011011000101111010000000110010111111101011001110001100111000110010101010100110111000110011101101111101001010111011100000010100000101001100100111101000100001111101110110111101111001000011';
redundancy = 100;
cycles = 1;
transmitted_stream_Array = double((transmitted_stream == '1'));

number_of_transmitted_bits = 1000 * cycles;

revamped_transmitted_bits = [];

for i = 1:number_of_transmitted_bits
% for i = 1:number_of_transmitted_bits
  
    for j = 1:redundancy
        revamped_transmitted_bits = [ revamped_transmitted_bits;transmitted_stream_Array(i)];
    end
end

                


% Calculating Pixel Intensities
    
for frame = 1 : numberOfFrames
        
        
        % Extract the frame from the movie structure.
        thisFrame = read(videoObject, frame);
        thisFrame = imcrop(thisFrame,pos_rect);
        
         % Calculate the mean gray level.
        grayImage = rgb2gray(thisFrame);
        meanGrayLevels(frame) = mean(grayImage(:));
        
        
        
        % Calculate the mean R, G, and B levels.
        meanRedLevels(frame) = mean(mean(thisFrame(:, :, 1)));
        meanGreenLevels(frame) = mean(mean(thisFrame(:, :, 2)));
        meanBlueLevels(frame) = mean(mean(thisFrame(:, :, 3)));
        
        % status of the processing 
        if mod(frame,1000) == 0
            
            fprintf('Processed frame %4d of %d.\n', frame, numberOfFrames);
        end
        
                   
end

clc; % for clearing status on command window




% THRESHOLD
threshold = sum(meanBlueLevels,'all')/numberOfFrames;



%=========================== Analyzed data from frames ====================

for frame = 1: numberOfFrames
       
    % recieved bits 
        bits(frame) = (meanBlueLevels(frame) >= threshold);
        thresholdlist(frame) = threshold;


end
        

% =================== CHANGE CSV FILE NAMES EVERY TIME ===================

%Location to where the csv files are stored

%---------------------------------------------------------------------------------------------------------------


save_table='/Users/sathwikchowda/Desktop/morselab/matlab-underwater/March-30-Results/march-30/1Hz_100fps_Vertical/';


%---------------------------------------------------------------------------------------------------------------



% ========== Exporting RAW Data and Position Coordinates to CSV Files =====

% Position Coordiantes
Positions = table(pos_rect(1),pos_rect(2),pos_rect(3),pos_rect(4), 'VariableNames',{'X-coordinates','Y-coordinates','Width','Height'});

table_path_format = [save_table '1Hz-position-coordinates.csv'];
writetable(Positions,table_path_format);

% Raw Data of all the Pixel Intensities and Bits
Intensities = table(meanRedLevels,meanBlueLevels,meanGreenLevels,meanGrayLevels,bits, 'VariableNames',{'Red-Pixel-Intensity','Blue-Pixel-Intensity','Green-Pixel-Intensity','Gray-Levels','BITS'});

table_path_format = [save_table '1Hz-info.csv'];
writetable(Intensities,table_path_format);

T = table(revamped_transmitted_bits, 'VariableNames',{'TransmittedBits'});

table_path_format = [save_table '1Hz-Transmitted-Bits.csv'];
writetable(T,table_path_format);


% ============================ PLOTTING ====================================

%Plot the pixel intensity levels.

        title('Pixel Intensity Graph', 'FontSize', fontSize);
		xlabel('Frame Number')
        ylabel('Pixel Intensity')
        hold off;
        hold on;           
        plot(meanRedLevels, 'r-', 'LineWidth', 2);
        plot(meanGreenLevels, 'g-', 'LineWidth', 2);
        plot(meanBlueLevels , 'b-', 'LineWidth', 2);
        grid on;
        
 %plot for only blue intensity
 
        figure();
        title(' Blue Pixel Intensity Graph', 'FontSize', fontSize);
		xlabel('Frame Number')
        ylabel('Blue Pixel Intensity')
        hold off;
        hold on;           
        plot(meanBlueLevels , 'b-', 'LineWidth', 2);
        h = yline(threshold, 'r--', 'LineWidth', 4);
        grid on;
        
        
% ============================ Deleting Variables ====================================      

% %For deleting un-wanted variables in workspace
% vars = {'fontSize','grayImage','h_rect','i','Intensities','j','Positions','save_table','T','table_path_format','thisFrame','videoObject','frame','pos_rect'};
% clear(vars{:})
% 
% clear vars;
clc; % for clearing status on command window

filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/meanBlueLevels.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const MEAN_BLUE_LEVELS = %s;', jsonencode(meanBlueLevels)));
fclose(fid);


filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/meanRedLevels.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const MEAN_RED_LEVELS = %s;',  jsonencode(meanRedLevels)));
fclose(fid);


filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/meanGreenLevels.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const MEAN_GREEN_LEVELS = %s;',  jsonencode(meanGreenLevels)));
fclose(fid);

filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/threshold.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const THRESHOLD = %s;',  jsonencode(thresholdlist)));
fclose(fid);
toc

filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/position.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const POSITION = %s;',  jsonencode(Positions)));
fclose(fid);
toc

filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/tranmsmitted_bits.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const TRANSMITTED_BITS = %s;',  jsonencode(revamped_transmitted_bits)));
fclose(fid);
toc

filename = "/Applications/XAMPP/xamppfiles/htdocs/underwater-website/graph-data/received_bits.js";
fid = fopen(filename,'w');
fprintf(fid, sprintf('const RECEIVED_BITS = %s;',  jsonencode(bits-0.5)));
fclose(fid);
toc
