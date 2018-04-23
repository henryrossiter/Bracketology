stats = csvread('training_data.csv',1,0);
tourney_wins = stats(:, 1);
season_games = stats(:, 3);
season_win_pct = stats(:, 4);
season_ppg = stats(:, 5);
const = ones(size(tourney_wins));
facs = horzcat(season_win_pct,season_games,season_ppg,const);

beta = mvregress(facs,tourney_wins,'algorithm','cwls');

cont_pred_outcomes = [];
disc_pred_outcomes = [];
posx = [];
posy = [];
posz = [];
ind = [1 1 1];
for z = 50:1:100
    ind(1) = 1;
    for x = .5:.01:1.0
        ind(2) = 1;
        for y = 20:.6:50
            true_val = beta(1).*x + beta(2).*y + beta(3).*z + beta(4);
            val = round(beta(1).*x + beta(2).*y + beta(3).*z + beta(4));
            if val<0
                val = 0;
                true_val = 0;
            elseif val >6
                val = 6;
                true_val = 6;
            end
            cont_pred_outcomes(ind(1),ind(2),ind(3)) = true_val;
            disc_pred_outcomes(ind(1),ind(2),ind(3)) = val;
            ind(2) = ind(2) +1;
        end  
        ind(1) = ind(1) + 1;
    end
    ind(3) = ind(3)+1;
end


h = figure;

view(3);
axis on;
grid on;

filename = 'cont_prediction.gif';
for n = 1:1:70
    az = 1.2*n+20;
    el = .4*n;
    view(az, el);
    zslice = 50+.4*n;
    xslice = .55+.006*n;
    yslice = [30 40];
    slice([.5:.01:1.0],[20:.6:50],[50:1:100],cont_pred_outcomes,xslice,yslice,zslice);
    xlabel('win pct')
    ylabel('games played')
    zlabel('ppg')
    cb = colorbar;
    cb.Label.String = 'predicted wins';
    az = n+30;
    el = .7*n+20;
    view(az, el);
    drawnow
      % Capture the plot as an image
      frame = getframe(h);
      im = frame2im(frame);
      [imind,cm] = rgb2ind(im,256);
      % Write to the GIF File
      if n == 1
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf,'DelayTime',.1);
      else
          imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',.1);
      end
end

filename = 'disc_prediction.gif';
for n = 1:.6:60
    az = 1.0*n+75;
    el = .4*n+15;
    view(az, el);
    zslice = 50+.4*n;
    xslice = [.55 .95];
    yslice = [30 40];
    slice([.5:.01:1.0],[20:.6:50],[50:1:100],disc_pred_outcomes,xslice,yslice,zslice);
    xlabel('win pct')
    ylabel('games played')
    zlabel('ppg')
    cb = colorbar;
    cb.Label.String = 'predicted wins';
    az = n+30;
    el = .7*n+20;
    view(az, el);
    drawnow
      % Capture the plot as an image
      frame = getframe(h);
      im = frame2im(frame);
      [imind,cm] = rgb2ind(im,256);
      % Write to the GIF File
      if n == 1
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf,'DelayTime',.1);
      else
          imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',.1);
      end
end