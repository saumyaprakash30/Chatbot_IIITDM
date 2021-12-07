import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageDictionaryComponent } from './recv-message-dictionary.component';

describe('RecvMessageDictionaryComponent', () => {
  let component: RecvMessageDictionaryComponent;
  let fixture: ComponentFixture<RecvMessageDictionaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageDictionaryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageDictionaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
