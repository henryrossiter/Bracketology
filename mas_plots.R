library(ggplot2)

dat <- read.csv('training_data.csv', header = TRUE)

plot <- ggplot(dat, aes(x=jitter(seed,3), y=jitter(tourney_wins,2.5))) + 
  geom_point()+
  geom_smooth(method=lm)+
  labs(x = 'seed', y = 'tournament games won')
  theme(axis.line = element_line(color = 'black'))
eq <- substitute(italic(r)^2~"="~r2, 
                 list(r2 = format(summary(m)$r.squared, digits = 3)))
text <- data.frame(eq = as.character(as.expression(eq)))
plot <- plot + geom_text(aes(label = eq,x =105, y=6), data = text, parse = TRUE, inherit.aes = FALSE)
plot
m <- lm(seed ~ tourney_wins, dat);
summary(m)

