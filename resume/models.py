from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns

# Create your models here.

EXP_CHOICES = ( 
    ("Training", "Training"), 
    ("Novice", "Novice"), 
    ("Intermediate", "Intermediate"), 
    ("Expert", "Expert"), 
)

class Skill(models.Model):
    """Model representing a skill."""
    
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=30)
    experience = models.CharField(max_length=30,
        choices = EXP_CHOICES, 
        default = 'Training',
        ) 

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Contribution(models.Model):
    """Model representing a job duty/contribution."""

    class Meta:
        ordering = ['description']

    description = models.CharField(max_length=200)
       
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.description
        
class Project(models.Model):
    """Model representing a project."""
    
    class Meta:
        ordering = ['name']
        
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    skill = models.ManyToManyField(Skill)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular project instance."""
        return reverse('project_detail', args=[str(self.id)])

    def get_skill(self):
        return ", ".join([p.name for p in self.skill.all()])
    get_skill.short_description = 'skill'

class Job(models.Model):
    """Model representing a job."""
    
    class Meta:
        ordering = ['start_date']
    
    name = models.CharField(max_length=40)
    skill = models.ManyToManyField(Skill)
    project = models.ManyToManyField(Project)
    description = models.CharField(max_length=200)
    remote_pct = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=40)
    company = models.CharField(max_length=30)
    client = models.CharField(max_length=40)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    contribution = models.ManyToManyField(Contribution)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
        
    def get_absolute_url(self):
        """Returns the url to access a particular job instance."""
        return reverse('job_detail', args=[str(self.id)])
        
    def get_conlist(self):
        jobcons = "|".join([p.description for p in self.contribution.all()])
        con_list = jobcons.split("|")
        for i, con in enumerate(con_list, 0):
            if len(con) > 90:
                cut = con[0:90].rfind(" ")
                con2 = con[cut+1:]
                con_list[i] = con[0:cut]
                con_list.insert(i+1, con2)
        return con_list
        
    def get_contribution(self):
        return "| ".join([p.description for p in self.contribution.all()])        
    get_contribution.short_description = 'contribution'

    def get_skill(self):
        return ", ".join([p.name for p in self.skill.all()])
    get_skill.short_description = 'skill'
        
    def get_project(self):
        return ", ".join([p.name for p in self.project.all()])
    get_project.short_description = 'project'
 
